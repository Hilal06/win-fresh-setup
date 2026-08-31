# Windows 11 Winget App Installer - PowerShell Launcher
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "         Windows 11 Winget App Installer Setup         " -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    $pyCmd = Get-Command py -ErrorAction SilentlyContinue
    if (-not $pyCmd) {
        Write-Host "[!] Python not found. Installing Python 3.12 via Winget..." -ForegroundColor Yellow
        winget install Python.Python.3.12 -e --accept-package-agreements --accept-source-agreements
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    }
}

# Setup venv
if (-not (Test-Path ".venv")) {
    Write-Host "[*] Creating Python virtual environment (.venv)..." -ForegroundColor Cyan
    python -m venv .venv
}

# Activate venv
if (Test-Path ".venv\Scripts\Activate.ps1") {
    & .\.venv\Scripts\Activate.ps1
}

# Install requirements
Write-Host "[*] Installing / Verifying requirements..." -ForegroundColor Cyan
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt

# Run installer
Write-Host "[*] Starting TUI Installer..." -ForegroundColor Green
python installer.py
