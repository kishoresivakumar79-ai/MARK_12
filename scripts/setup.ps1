# MARK 12 Setup Script for PowerShell
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  ⚡ Setting up MARK 12 Assistant ⚡" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

$pythonExe = "C:\Users\RYZEN\AppData\Local\Programs\Python\Python310\python.exe"
if (-not (Test-Path $pythonExe)) {
    $pythonExe = "python"
}

Write-Host "1. Initializing SQLite Database..." -ForegroundColor Yellow
& $pythonExe "database\init_db.py"

Write-Host "2. Creating Default Admin Credentials..." -ForegroundColor Yellow
& $pythonExe "scripts\create_admin.py" admin jarvis2026

Write-Host "`nMARK 12 setup complete! Run .\scripts\start.ps1 to start the system." -ForegroundColor Green
