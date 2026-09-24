@echo off
rem ============================================
rem  GABUNG Projek Kriptografi 1 — klik dua kali
rem  (versi offline: pakai join.ps1 yang sudah
rem   ada di folder yang SAMA dengan file ini)
rem ============================================
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0join-local.ps1"
echo.
pause
