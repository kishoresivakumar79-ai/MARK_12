@echo off
title MARK 12 AI Operating System
cd /d "%~dp0\.."
echo =======================================================
echo   Launching MARK 12 AI Operating System
echo =======================================================
"C:\Users\RYZEN\AppData\Local\Programs\Python\Python310\python.exe" -m backend.main
if %ERRORLEVEL% NEQ 0 (
    python -m backend.main
)
pause
