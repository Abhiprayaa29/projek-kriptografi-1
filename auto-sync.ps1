# Auto-commit + auto-push + auto-pull setiap ada perubahan di folder ini.
# Untuk Windows. Dijalankan oleh Scheduled Task: autosync-projek-kriptografi
# Jalankan: powershell -NoProfile -ExecutionPolicy Bypass -File .\auto-sync.ps1
$ErrorActionPreference = 'Continue'

$RepoDir   = $PSScriptRoot
$LogFile   = Join-Path $RepoDir '.autosync.log'
$IntervalSec = 2
$SettleSec   = 1

$mutex = New-Object System.Threading.Mutex($false, 'Local\autosync-projek-kriptografi')
if (-not $mutex.WaitOne(0)) {
    # Sudah ada instance lain yang jalan.
    exit 0
}

function Write-Log {
    param([string]$Message)
    $line = '{0} {1}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Message
    Add-Content -LiteralPath $LogFile -Value $line -Encoding UTF8
}

function Get-Head { (git rev-parse HEAD 2>$null) }
function Get-Status { @(git status --porcelain 2>$null) }

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

        # Selalu coba selaraskan dengan GitHub (push kalau lokal unggah,
        # pull kalau remote unggah / keduanya).
        $before = Get-Head
        git pull --rebase --autostash 2>$null | Out-Null
        git push 2>$null | Out-Null
        $after  = Get-Head

        if ($dirty) {
            if ($LASTEXITCODE -eq 0) {
                Write-Log "PUSHED: $changed"
            }
            else {
                Write-Log "COMMIT_OK_PUSH_FAIL (offline / conflict?): $changed"
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
