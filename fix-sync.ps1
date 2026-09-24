# Fix otomatis: pull fix terbaru, restart watcher, lalu diagnosa.
# Jalankan sekali dari folder repo:
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\fix-sync.ps1
$ErrorActionPreference = 'Continue'
$RepoDir = $PSScriptRoot
$TaskName = 'autosync-projek-kriptografi'
$LogFile = Join-Path $RepoDir '.autosync.log'

Set-Location -LiteralPath $RepoDir
Write-Host '=== 1/4 git pull --rebase ===' -ForegroundColor Cyan
git pull --rebase
if ($LASTEXITCODE -ne 0) {
    Write-Host 'pull gagal - cek pesan di atas' -ForegroundColor Red
}

Write-Host ''
Write-Host ('=== 2/4 restart task {0} ===' -f $TaskName) -ForegroundColor Cyan
Stop-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
Start-ScheduledTask -TaskName $TaskName
Write-Host 'task di-restart; tunggu ~10 detik biar watcher jalan...' -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ''
Write-Host '=== 3/4 cek-sync.ps1 ===' -ForegroundColor Cyan
$cek = Join-Path $RepoDir 'cek-sync.ps1'
if (Test-Path -LiteralPath $cek) {
    & powershell -NoProfile -ExecutionPolicy Bypass -File $cek
} else {
    Write-Host 'cek-sync.ps1 tidak ada, lewati' -ForegroundColor Yellow
}

Write-Host ''
Write-Host '=== 4/4 log terakhir (.autosync.log) ===' -ForegroundColor Cyan
if (Test-Path -LiteralPath $LogFile) {
    Get-Content -LiteralPath $LogFile -Tail 30
} else {
    Write-Host 'log belum ada' -ForegroundColor Yellow
}

Write-Host ''
Write-Host '=== SELESAI - paste semua hasil di atas ke chat ===' -ForegroundColor Green
