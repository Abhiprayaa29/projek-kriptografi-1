# Auto-commit + auto-push + auto-pull setiap ada perubahan di folder ini.
# Untuk Windows. Dijalankan oleh Scheduled Task: autosync-projek-kriptografi
# Jalankan: powershell -NoProfile -ExecutionPolicy Bypass -File .\auto-sync.ps1
$ErrorActionPreference = 'Continue'

# Jangan pernah menunggu prompt di jendela Hidden Scheduled Task:
# gagal cepat + masuk log, bukan hang tanpa jejak.
$env:GIT_TERMINAL_PROMPT = '0'
$env:GCM_INTERACTIVE     = 'Never'
$env:GIT_ASKPASS         = 'echo'

$RepoDir   = $PSScriptRoot
$LogFile   = Join-Path $RepoDir '.autosync.log'
$IntervalSec = 2
$SettleSec   = 1
$ErrFile     = Join-Path $env:TEMP ("autosync-git-err-{0}.txt" -f $PID)

$mutex = New-Object System.Threading.Mutex($false, 'Local\autosync-projek-kriptografi')
if (-not $mutex.WaitOne(0)) {
    exit 0
}

function Write-Log {
    param([string]$Message)
    $line = '{0} {1}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Message
    Add-Content -LiteralPath $LogFile -Value $line -Encoding UTF8
}

function Invoke-Git {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$GitArgs)
    if (Test-Path -LiteralPath $ErrFile) {
        Remove-Item -LiteralPath $ErrFile -Force -ErrorAction SilentlyContinue
    }
    $null = & git @GitArgs 2>$ErrFile
    $code = $LASTEXITCODE
    $err  = ''
    if (Test-Path -LiteralPath $ErrFile) {
        $err = (Get-Content -LiteralPath $ErrFile -Raw -ErrorAction SilentlyContinue)
        if ($err) { $err = $err.Trim() }
        Remove-Item -LiteralPath $ErrFile -Force -ErrorAction SilentlyContinue
    }
    [pscustomobject]@{ Code = $code; Err = $err }
}

function Get-Head {
    $r = Invoke-Git rev-parse HEAD
    if ($r.Code -eq 0 -and $r.Err -eq '') {
        (& git rev-parse HEAD 2>$null)
    } else {
        $null
    }
}

function Get-Status { @(git status --porcelain 2>$null) }

function Write-FailOnce {
    <# Log galat hanya saat pesan berubah atau tiap ~30 kegagalan (~1 menit). #>
    param(
        [string]$Kind,
        [string]$Message,
        [ref]$LastMsg,
        [ref]$Count
    )
    $Count.Value = [int]$Count.Value + 1
    $msg = if ($Message) { $Message } else { 'galat tidak diketahui' }
    $short = ($msg -split "`r?`n" | Select-Object -First 3) -join ' | '
    if ($short.Length -gt 400) { $short = $short.Substring(0, 400) }
    if ($Count.Value -eq 1 -or $short -ne $LastMsg.Value -or ($Count.Value % 30) -eq 0) {
        Write-Log ("{0} FAIL (x{1}): {2}" -f $Kind, $Count.Value, $short)
        $LastMsg.Value = $short
    }
}

$script:lastPullErr = ''
$script:lastPushErr = ''
$script:pullFailN   = 0
$script:pushFailN   = 0

Set-Location -LiteralPath $RepoDir
Write-Log ("watcher started (pid {0})" -f $PID)

while ($true) {
    try {
        $status = Get-Status
        $dirty  = $status.Count -gt 0

        if ($dirty) {
            Start-Sleep -Seconds $SettleSec
            $status = Get-Status
            $dirty  = $status.Count -gt 0
        }

        $changed = ''
        if ($dirty) {
            $changed = (($status | Select-Object -First 20) -join '; ')
            git add -A 2>$null | Out-Null

            $name = git config user.name 2>$null
            if (-not $name) { $name = 'unknown' }

            $msg = 'auto-sync: {0} [{1}]' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $name
            git commit -m $msg 2>$null | Out-Null
        }

        $before = Get-Head

        $pull = Invoke-Git pull --rebase --autostash
        if ($pull.Code -ne 0) {
            Write-FailOnce -Kind 'PULL' -Message $pull.Err -LastMsg ([ref]$script:lastPullErr) -Count ([ref]$script:pullFailN)
        } else {
            $script:pullFailN   = 0
            $script:lastPullErr = ''
        }

        $push = Invoke-Git push
        $pushOk = ($push.Code -eq 0)
        if (-not $pushOk) {
            Write-FailOnce -Kind 'PUSH' -Message $push.Err -LastMsg ([ref]$script:lastPushErr) -Count ([ref]$script:pushFailN)
        } else {
            $script:pushFailN   = 0
            $script:lastPushErr = ''
        }

        $after = Get-Head

        if ($dirty) {
            if ($pushOk) {
                Write-Log "PUSHED: $changed"
            } else {
                Write-Log "COMMIT_OK_PUSH_FAIL: $changed"
            }
        }
        elseif ($before -and $after -and $before -ne $after) {
            Write-Log 'PULLED: update dari GitHub'
        }
    }
    catch {
        Write-Log ("ERROR: {0}" -f $_.Exception.Message)
    }

    Start-Sleep -Seconds $IntervalSec
}
