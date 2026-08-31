# win-fresh-setup - 1-Line Online Web Bootstrap Installer
# Run in PowerShell: irm https://raw.githubusercontent.com/Hilal06/win-fresh-setup/main/bootstrap.ps1 | iex

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 -bor [Net.SecurityProtocolType]::Tls13
$ErrorActionPreference = "Stop"

Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "       win-fresh-setup: Online Web Bootstrap           " -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host ""

# Check Winget
$wingetCmd = Get-Command winget -ErrorAction SilentlyContinue
if (-not $wingetCmd) {
    Write-Host "[!] Winget is not detected. Please make sure App Installer is updated from Microsoft Store." -ForegroundColor Yellow
}

$tempFolder = Join-Path $env:TEMP "win-fresh-setup"
$zipPath = Join-Path $env:TEMP "win-fresh-setup.zip"

if (Test-Path $tempFolder) {
    Remove-Item -Path $tempFolder -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host "[*] Downloading latest win-fresh-setup from GitHub..." -ForegroundColor Cyan
$repoUrl = "https://github.com/Hilal06/win-fresh-setup/archive/refs/heads/main.zip"

try {
    Invoke-WebRequest -Uri $repoUrl -OutFile $zipPath -UseBasicParsing
    Write-Host "[*] Extracting setup files..." -ForegroundColor Cyan
    Expand-Archive -Path $zipPath -DestinationPath $tempFolder -Force
    Remove-Item -Path $zipPath -Force

    $extractedDir = Join-Path $tempFolder "win-fresh-setup-main"
    if (Test-Path $extractedDir) {
        Set-Location $extractedDir
    } else {
        Set-Location $tempFolder
    }

    Write-Host "[✓] Setup ready. Launching installer..." -ForegroundColor Green
    & .\run.ps1
}
catch {
    Write-Host "[X] Failed to download or execute setup: $_" -ForegroundColor Red
}
