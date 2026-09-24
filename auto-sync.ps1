# Auto-commit + auto-push setiap ada perubahan file di folder ini.
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

Set-Location -LiteralPath $RepoDir
Write-Log ("watcher started (pid {0})" -f $PID)

while ($true) {
    try {
        $status = @(git status --porcelain 2>$null)
        if ($status.Count -gt 0) {
            Start-Sleep -Seconds $SettleSec
            $status = @(git status --porcelain 2>$null)
            if ($status.Count -gt 0) {
                $changed = (($status | Select-Object -First 20) -join '; ')

                git add -A 2>$null | Out-Null

                $name = git config user.name 2>$null
                if (-not $name) { $name = 'unknown' }

                $msg = 'auto-sync: {0} [{1}]' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $name
                git commit -m $msg 2>$null | Out-Null

                git pull --rebase --autostash 2>$null | Out-Null
                git push 2>$null | Out-Null
                if ($LASTEXITCODE -eq 0) {
                    Write-Log "PUSHED: $changed"
                }
                else {
                    git pull --rebase --autostash 2>$null | Out-Null
                    git push 2>$null | Out-Null
                    if ($LASTEXITCODE -eq 0) {
                        Write-Log "PUSHED_AFTER_REBASE: $changed"
                    }
                    else {
                        Write-Log "COMMIT_OK_PUSH_FAIL (offline / conflict?): $changed"
                    }
                }
            }
        }
        else {
            # Lokal bersih → tarik update teman (folder/file baru di GitHub).
            $before = git rev-parse HEAD 2>$null
            git pull --rebase --autostash --ff-only 2>$null | Out-Null
            $after = git rev-parse HEAD 2>$null
            if ($LASTEXITCODE -eq 0 -and $before -and $after -and $before -ne $after) {
                Write-Log 'PULLED: update dari GitHub'
            }
        }
    }
    catch {
        Write-Log ("ERROR: {0}" -f $_.Exception.Message)
    }

    Start-Sleep -Seconds $IntervalSec
}
