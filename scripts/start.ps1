# MARK 12 Launcher for PowerShell
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  ⚡ Launching MARK 12 AI Operating System ⚡" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

$pythonExe = "C:\Users\RYZEN\AppData\Local\Programs\Python\Python310\python.exe"
if (-not (Test-Path $pythonExe)) {
    $pythonExe = "python"
}

# Run the master server
& $pythonExe -m backend.main
