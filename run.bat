@echo off
title OkbaTrack
cd /d "%~dp0"
echo [*] Checking dependencies...
"%~dp0venv\Scripts\python.exe" OkbaTrack.py 2>nul
if %errorlevel% neq 0 (
    where python >nul 2>nul
    if %errorlevel% neq 0 (
        echo [!] Python not found. Install it from https://python.org
        pause
        exit /b
    )
    python GhostTR.py
)
pause
