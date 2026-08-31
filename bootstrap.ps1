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

$originalLocation = Get-Location
$tempFolder = Join-Path $env:TEMP "win-fresh-setup"
$zipPath = Join-Path $env:TEMP "win-fresh-setup.zip"

try {
    if (Test-Path $tempFolder) {
        Remove-Item -Path $tempFolder -Recurse -Force -ErrorAction SilentlyContinue
    }

    Write-Host "[*] Downloading latest win-fresh-setup from GitHub..." -ForegroundColor Cyan
    $repoUrl = "https://github.com/Hilal06/win-fresh-setup/archive/refs/heads/main.zip"

    Invoke-WebRequest -Uri $repoUrl -OutFile $zipPath -UseBasicParsing
    Write-Host "[*] Extracting setup files..." -ForegroundColor Cyan
    Expand-Archive -Path $zipPath -DestinationPath $tempFolder -Force
    if (Test-Path $zipPath) {
        Remove-Item -Path $zipPath -Force -ErrorAction SilentlyContinue
    }

    $extractedDir = Join-Path $tempFolder "win-fresh-setup-main"
    if (Test-Path $extractedDir) {
        Set-Location $extractedDir
    } else {
        Set-Location $tempFolder
    }

    Write-Host "[✓] Setup ready. Launching installer..." -ForegroundColor Green
    Write-Host ""
    & .\run.ps1
}
catch {
    Write-Host "[X] Error during setup execution: $_" -ForegroundColor Red
}
finally {
    # Move out of the temp folder so file handles are released
    Set-Location $originalLocation
    
    # Clean up temporary downloaded archive and directory
    if (Test-Path $zipPath) {
        Remove-Item -Path $zipPath -Force -ErrorAction SilentlyContinue
    }
    if (Test-Path $tempFolder) {
        Write-Host ""
        Write-Host "[*] Cleaning up temporary setup files in $tempFolder..." -ForegroundColor Cyan
        # Brief pause to ensure all process handles released
        Start-Sleep -Milliseconds 500
        Remove-Item -Path $tempFolder -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "[✓] Cleanup complete. No leftover files remained on your system!" -ForegroundColor Green
    }
}
