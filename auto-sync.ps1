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
$GitTimeoutSec = 45

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
    # PS 5.1: jangan campur ValueFromRemainingArguments + param typed lain
    # (argumen positional seperti "pull" bisa salah diikat ke param typed).
    # Semua argumen git masuk lewat named -Args; timeout via -Timeout (opsional).
    param(
        [Parameter(Mandatory = $true)][string[]]$Args,
        [int]$Timeout = 0
    )
    $TimeoutSec = if ($Timeout -gt 0) { $Timeout } else { $GitTimeoutSec }

    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = 'git'
    $argLine = ($Args | ForEach-Object {
        if ($_ -match '[\s"]') { '"' + ($_ -replace '"', '\"') + '"' } else { $_ }
    }) -join ' '
    $psi.Arguments = $argLine
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.CreateNoWindow = $true
    $psi.WorkingDirectory = $RepoDir

    $proc = $null
    try {
        $proc = [System.Diagnostics.Process]::Start($psi)
    } catch {
        return [pscustomobject]@{ Code = -1; Out = ''; Err = ("gagal start git: {0}" -f $_.Exception.Message) }
    }
    if (-not $proc) {
        return [pscustomobject]@{ Code = -1; Out = ''; Err = 'gagal start git' }
    }

    $outTask = $proc.StandardOutput.ReadToEndAsync()
    $errTask = $proc.StandardError.ReadToEndAsync()

    if (-not $proc.WaitForExit($TimeoutSec * 1000)) {
        try { $proc.Kill() } catch { }
        $null = $proc.WaitForExit(3000)
        try { $proc.Dispose() } catch { }
        return [pscustomobject]@{
            Code = -1
            Out  = ''
            Err  = ("timeout after {0}s (proses git di-kill)" -f $TimeoutSec)
        }
    }

    $null = $outTask.Wait(2000)
    $null = $errTask.Wait(2000)

    $out = ''
    $err = ''
    try { if ($outTask.IsCompleted) { $out = $outTask.Result } } catch { }
    try { if ($errTask.IsCompleted) { $err = $errTask.Result } } catch { }

    $code = $proc.ExitCode
    try { $proc.Dispose() } catch { }

    if ($out) { $out = $out.Trim() }
    if ($err) { $err = $err.Trim() }
    [pscustomobject]@{ Code = $code; Out = $out; Err = $err }
}

function Get-Head {
    $r = Invoke-Git -Args @('rev-parse', 'HEAD') -Timeout 15
    if ($r.Code -eq 0 -and $r.Out) { $r.Out } else { $null }
}

function Get-AheadCount {
    $r = Invoke-Git -Args @('rev-list', '--count', 'origin/main..HEAD') -Timeout 15
    if ($r.Code -eq 0 -and $r.Out -match '^\d+$') { [int]$r.Out } else { 0 }
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

        $pull = Invoke-Git -Args @('pull', '--rebase', '--autostash')
        if ($pull.Code -ne 0) {
            Write-FailOnce -Kind 'PULL' -Message $pull.Err -LastMsg ([ref]$script:lastPullErr) -Count ([ref]$script:pullFailN)
        } else {
            $script:pullFailN   = 0
            $script:lastPullErr = ''
        }

        # Hitung ahead SEBELUM push: dipakai untuk log push yang sukses
        # padahal tree bersih (tanpa ini, push no-op/commit lokal tidak pernah muncul di log).
        $aheadBefore = Get-AheadCount

        $push = Invoke-Git -Args @('push')
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
        elseif ($aheadBefore -gt 0 -and $pushOk) {
            Write-Log ("PUSHED: push {0} commit lokal (tree bersih)" -f $aheadBefore)
        }
    }
    catch {
        Write-Log ("ERROR: {0}" -f $_.Exception.Message)
    }

    Start-Sleep -Seconds $IntervalSec
}
