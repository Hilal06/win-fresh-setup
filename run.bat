@echo off
setlocal enabledelayedexpansion
title Windows 11 Winget App Installer

cd /d "%~dp0"

echo =======================================================
echo          Windows 11 Winget App Installer Setup
echo =======================================================
echo.

:: 1. Check for Python
where python >nul 2>&1
if !ERRORLEVEL! NEQ 0 (
    where py >nul 2>&1
    if !ERRORLEVEL! NEQ 0 (
        if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
            set "PATH=%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python312\Scripts;!PATH!"
        ) else (
            echo [!] Python is not found on your system.
            echo [*] Installing Python 3.12 automatically via Winget...
            echo.
            winget install Python.Python.3.12 -e --accept-package-agreements --accept-source-agreements
            if !ERRORLEVEL! NEQ 0 (
                echo [X] Failed to install Python automatically.
                echo     Please install Python from https://www.python.org/downloads/ and check "Add Python to PATH".
                pause
                exit /b 1
            )
            echo [OK] Python installed. Refreshing environment...
            set "PATH=%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python312\Scripts;!PATH!"
        )
    )
)

:: 2. Setup Virtual Environment (if needed)
if not exist ".venv" (
    echo [*] Creating Python virtual environment .venv...
    python -m venv .venv
)

:: 3. Activate venv & Install dependencies
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

echo [*] Checking dependencies...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt

:: 4. Run Installer TUI
echo [*] Launching Winget App Installer TUI...
echo.
python installer.py

if !ERRORLEVEL! NEQ 0 (
    echo.
    echo Script ended with exit code !ERRORLEVEL!.
    pause
)
