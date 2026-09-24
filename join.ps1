# Join Projek Kriptografi 1 — plug & play untuk anggota kelompok (Windows).
# Dipanggil via:
#   irm https://raw.githubusercontent.com/Abhiprayaa29/projek-kriptografi-1/main/join.ps1 | iex
# CATATAN: saat di-irm|iex, $PSScriptRoot kosong — script ini wajib self-contained
# sampai repo berhasil di-clone ke disk.
$ErrorActionPreference = 'Stop'

$RepoUrl   = 'https://github.com/Abhiprayaa29/projek-kriptografi-1.git'
$ParentDir = Join-Path $env:USERPROFILE 'Documents\Kuliah\semester-5'
$TargetDir = Join-Path $ParentDir 'kriptografi'

# Kalau script dijalankan dari dalam clone yang sudah ada (GABUNG.bat / -File),
# pakai folder itu — jangan clone ulang ke Documents.
if ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot '.git'))) {
    $TargetDir = $PSScriptRoot
    $ParentDir = Split-Path -Parent $TargetDir
}

function Refresh-Path {
    $machine = [Environment]::GetEnvironmentVariable('Path', 'Machine')
    $user    = [Environment]::GetEnvironmentVariable('Path', 'User')
    $env:Path = "$machine;$user"
}

function Test-Git {
    return [bool](Get-Command git -ErrorAction SilentlyContinue)
}

function Ensure-Git {
    if (Test-Git) { return }

    Write-Host ''
    Write-Host 'Git belum terpasang. Mencoba install otomatis via winget...' -ForegroundColor Yellow

    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install --id Git.Git -e --source winget `
            --accept-package-agreements --accept-source-agreements
        Refresh-Path
        if (Test-Git) {
            Write-Host 'Git terpasang.' -ForegroundColor Green
            return
        }
    }

    Write-Host 'Install manual: buka halaman download Git, install dengan default, lalu tutup installer.' -ForegroundColor Yellow
    Start-Process 'https://git-scm.com/download/win'
    do {
        Read-Host 'Tekan Enter SETELAH Git selesai diinstall'
        Refresh-Path
    } while (-not (Test-Git))
}

# Tanpa prompt: identitas diisi otomatis biar benar-benar plug & play.
function Ensure-GitIdentity {
    $name  = git config --global user.name  2>$null
    $email = git config --global user.email 2>$null
    if ($name -and $email) { return }

    # Prioritas: username GitHub (gh) -> nama user Windows
    $name = $null
    $email = $null
    if (Get-Command gh -ErrorAction SilentlyContinue) {
        $login = gh api user --jq .login 2>$null
        if ($login) {
            $name  = $login
            $email = "$login@users.noreply.github.com"
        }
    }
    if (-not $name) {
        $name  = [Environment]::UserName
        $email = ($name.ToLower() -replace '[^a-z0-9-]', '') + '@users.noreply.github.com'
    }

    git config --global user.name $name
    git config --global user.email $email
    Write-Host ''
    Write-Host ("Identitas commit otomatis: {0} <{1}>" -f $name, $email) -ForegroundColor Green
}

function Ensure-Repo {
    if (Test-Path (Join-Path $TargetDir '.git')) {
        Write-Host "Repo sudah ada di: $TargetDir" -ForegroundColor Green
        return
    }

    Write-Host ''
    Write-Host "Clone repo ke: $TargetDir" -ForegroundColor Cyan
    New-Item -ItemType Directory -Force -Path $ParentDir | Out-Null
    git clone $RepoUrl $TargetDir
    if ($LASTEXITCODE -ne 0) {
        throw 'git gagal clone. Cek koneksi / akses collaborator ke repo.'
    }
}

function Invoke-AutoSyncSetup {
    $setup = Join-Path $TargetDir 'setup-autosync.ps1'
    if (-not (Test-Path $setup)) {
        throw "setup-autosync.ps1 tidak ditemukan di $setup"
    }
    Write-Host ''
    Write-Host 'Memasang auto-sync (Scheduled Task)...' -ForegroundColor Cyan
    & powershell -NoProfile -ExecutionPolicy Bypass -File $setup
}

function Open-VsCode {
    if (Get-Command code -ErrorAction SilentlyContinue) {
        code $TargetDir
        return
    }

    Write-Host ''
    Write-Host 'VS Code belum terpasang. Membuka halaman download...' -ForegroundColor Yellow
    Start-Process 'https://code.visualstudio.com'
    Write-Host 'Install VS Code dengan default, lalu buka folder:' -ForegroundColor Yellow
    Write-Host "  code `"$TargetDir`""
}

Write-Host '========================================' -ForegroundColor Cyan
Write-Host ' Join Projek Kriptografi 1 (Windows)'    -ForegroundColor Cyan
Write-Host '========================================' -ForegroundColor Cyan

Ensure-Git
Ensure-GitIdentity
Ensure-Repo
Invoke-AutoSyncSetup
Open-VsCode

Write-Host ''
Write-Host 'SELESAI — plug & play.' -ForegroundColor Green
Write-Host "Folder : $TargetDir"
Write-Host "Log    : $TargetDir\.autosync.log"
Write-Host ''
Write-Host 'Cara pakai: simpan file di VS Code (Ctrl+S) -> otomatis push ke GitHub.' -ForegroundColor Green
Write-Host ''
Read-Host 'Tekan Enter untuk tutup jendela ini'
