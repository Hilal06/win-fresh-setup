@echo off
setlocal enabledelayedexpansion
title Windows 11 Winget App Installer

cd /d "%~dp0"

echo =======================================================
echo          Windows 11 Winget App Installer Setup
echo =======================================================
echo.

:: 1. Check for Modern PowerShell (PowerShell 7+)
set "PWSH_EXE="
where pwsh >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    set "PWSH_EXE=pwsh"
) else (
    if exist "%ProgramFiles%\PowerShell\7\pwsh.exe" (
        set "PWSH_EXE=%ProgramFiles%\PowerShell\7\pwsh.exe"
    ) else if exist "%ProgramFiles(x86)%\PowerShell\7\pwsh.exe" (
        set "PWSH_EXE=%ProgramFiles(x86)%\PowerShell\7\pwsh.exe"
    ) else if exist "%LOCALAPPDATA%\Microsoft\PowerShell\7\pwsh.exe" (
        set "PWSH_EXE=%LOCALAPPDATA%\Microsoft\PowerShell\7\pwsh.exe"
    )
)

:: If Modern PowerShell is not found, install it via Winget
if not defined PWSH_EXE (
    echo [!] Modern PowerShell (PowerShell 7+) is not detected in this CMD session.
    echo [*] Installing latest Microsoft PowerShell via Winget...
    echo.
    winget install Microsoft.PowerShell -e --accept-package-agreements --accept-source-agreements
    if exist "%ProgramFiles%\PowerShell\7\pwsh.exe" (
        set "PWSH_EXE=%ProgramFiles%\PowerShell\7\pwsh.exe"
    ) else if exist "%ProgramFiles(x86)%\PowerShell\7\pwsh.exe" (
        set "PWSH_EXE=%ProgramFiles(x86)%\PowerShell\7\pwsh.exe"
    ) else (
        where pwsh >nul 2>&1
        if !ERRORLEVEL! EQU 0 set "PWSH_EXE=pwsh"
    )
)

:: If Modern PowerShell is available, transition execution to pwsh
if defined PWSH_EXE (
    echo [OK] Modern PowerShell detected: !PWSH_EXE!
    echo [*] Switching execution to modern PowerShell 7...
    echo.
    "!PWSH_EXE!" -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1"
    exit /b !ERRORLEVEL!
)

:: 2. Fallback: Run directly with Python if Modern PowerShell is not available
echo [!] Modern PowerShell not available. Continuing with Python setup in CMD...
echo.

:: Test if python in PATH actually executes (not MS Store alias)
python -c "import sys; print(sys.executable)" >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    set "PYTHON_EXE=python"
    goto :PYTHON_FOUND
)

:: Test if py launcher works
py -3 -c "import sys; print(sys.executable)" >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    set "PYTHON_EXE=py -3"
    goto :PYTHON_FOUND
)

:: Test known standard paths
for %%V in (Python313 Python312 Python311 Python310) do (
    if exist "%LOCALAPPDATA%\Programs\Python\%%V\python.exe" (
        set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\%%V\python.exe"
        set "PATH=%LOCALAPPDATA%\Programs\Python\%%V;%LOCALAPPDATA%\Programs\Python\%%V\Scripts;!PATH!"
        goto :PYTHON_FOUND
    )
    if exist "%ProgramFiles%\Python\%%V\python.exe" (
        set "PYTHON_EXE=%ProgramFiles%\Python\%%V\python.exe"
        set "PATH=%ProgramFiles%\Python\%%V;%ProgramFiles%\Python\%%V\Scripts;!PATH!"
        goto :PYTHON_FOUND
    )
    if exist "%ProgramFiles%\%%V\python.exe" (
        set "PYTHON_EXE=%ProgramFiles%\%%V\python.exe"
        set "PATH=%ProgramFiles%\%%V;%ProgramFiles%\%%V\Scripts;!PATH!"
        goto :PYTHON_FOUND
    )
    if exist "C:\%%V\python.exe" (
        set "PYTHON_EXE=C:\%%V\python.exe"
        set "PATH=C:\%%V;C:\%%V\Scripts;!PATH!"
        goto :PYTHON_FOUND
    )
)

:: If still not found, install via Winget
echo [!] Python was not found or is an unconfigured Windows Store shim.
echo [*] Installing Python 3.12 automatically via Winget...
echo.
winget install Python.Python.3.12 -e --accept-package-agreements --accept-source-agreements
if !ERRORLEVEL! NEQ 0 (
    echo [X] Failed to install Python automatically via Winget.
    echo     Please install Python from https://www.python.org/downloads/ and check "Add Python to PATH".
    pause
    exit /b 1
)

echo [OK] Python installed. Searching for installed executable...
for %%V in (Python313 Python312 Python311 Python310) do (
    if exist "%LOCALAPPDATA%\Programs\Python\%%V\python.exe" (
        set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\%%V\python.exe"
        set "PATH=%LOCALAPPDATA%\Programs\Python\%%V;%LOCALAPPDATA%\Programs\Python\%%V\Scripts;!PATH!"
        goto :PYTHON_FOUND
    )
    if exist "%ProgramFiles%\Python\%%V\python.exe" (
        set "PYTHON_EXE=%ProgramFiles%\Python\%%V\python.exe"
        set "PATH=%ProgramFiles%\Python\%%V;%ProgramFiles%\Python\%%V\Scripts;!PATH!"
        goto :PYTHON_FOUND
    )
)

:: Re-test PATH
python -c "import sys; print(sys.executable)" >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    set "PYTHON_EXE=python"
    goto :PYTHON_FOUND
)

echo [X] Could not locate installed Python binary. Please restart terminal.
pause
exit /b 1

:PYTHON_FOUND
echo [OK] Python found: !PYTHON_EXE!

:: 2. Setup Virtual Environment (if needed)
if not exist ".venv\Scripts\python.exe" (
    if exist ".venv" (
        echo [!] Rebuilding broken virtual environment...
        rmdir /s /q ".venv" >nul 2>&1
    )
    echo [*] Creating Python virtual environment (.venv)...
    !PYTHON_EXE! -m venv .venv
)

set "VENV_PYTHON=.venv\Scripts\python.exe"
if not exist "!VENV_PYTHON!" (
    set "VENV_PYTHON=!PYTHON_EXE!"
)

:: 3. Dependencies
echo [*] Checking dependencies...
!VENV_PYTHON! -m pip install --quiet --upgrade pip
!VENV_PYTHON! -m pip install --quiet -r requirements.txt

:: 4. Run Installer TUI
echo [*] Launching Winget App Installer TUI...
echo.
!VENV_PYTHON! installer.py

if !ERRORLEVEL! NEQ 0 (
    echo.
    echo Script ended with exit code !ERRORLEVEL!.
    pause
)

