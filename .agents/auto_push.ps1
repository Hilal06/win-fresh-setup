<#
.SYNOPSIS
    Automated Test-Driven Git Commit and Push Tool for win-fresh-setup.
.DESCRIPTION
    1. Sets workspace context to the repository root.
    2. Runs the test suite (test_installer.py).
    3. If tests FAIL: Halts execution immediately and displays failure diagnostics.
    4. If tests PASS: Stages all changes, commits with message, and pushes to origin.
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\.agents\auto_push.ps1 -CommitMessage "fix: update scripts"
#>

param(
    [string]$CommitMessage = ""
)

$ErrorActionPreference = "Stop"
$agentDir = $PSScriptRoot
$repoRoot = Split-Path -Parent $agentDir

# Ensure working directory is the repository root
Set-Location $repoRoot

Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "     win-fresh-setup: Automated Test and Push Tool     " -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host ("[*] Repository Root: " + $repoRoot) -ForegroundColor Gray
Write-Host ""

# 1. Locate Python executable
$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
$pythonExe = if (Test-Path $venvPython) { $venvPython } else { "python" }

Write-Host ("[*] Executing automated test suite with: " + $pythonExe) -ForegroundColor Cyan
Write-Host ""

$testScript = Join-Path $repoRoot "test_installer.py"
$testOutput = & $pythonExe $testScript 2>&1
$testExitCode = $LASTEXITCODE

# Display test output
$testOutput | ForEach-Object { Write-Host $_ }

if ($testExitCode -ne 0) {
    Write-Host ""
    Write-Host "=======================================================" -ForegroundColor Red
    Write-Host (" [X] TEST SUITE FAILED (Exit Code: " + $testExitCode + ")") -ForegroundColor Red
    Write-Host " Commit and Push aborted to prevent breaking changes!  " -ForegroundColor Red
    Write-Host " Please resolve the issues above before pushing.      " -ForegroundColor Red
    Write-Host "=======================================================" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=======================================================" -ForegroundColor Green
Write-Host " [OK] ALL TESTS PASSED! Proceeding with Commit and Push" -ForegroundColor Green
Write-Host "=======================================================" -ForegroundColor Green
Write-Host ""

# 2. Check Git status
$gitStatus = git status --porcelain
if (-not $gitStatus) {
    Write-Host "[!] Working tree clean. No changes to commit." -ForegroundColor Yellow
    exit 0
}

# 3. Determine commit message
if ([string]::IsNullOrWhiteSpace($CommitMessage)) {
    $defaultMsg = "chore: move automation tools to .agents directory"
    $inputMsg = Read-Host "Enter commit message (Press Enter for default: '$defaultMsg')"
    if ([string]::IsNullOrWhiteSpace($inputMsg)) {
        $CommitMessage = $defaultMsg
    } else {
        $CommitMessage = $inputMsg
    }
}

# 4. Stage, Commit, and Push
Write-Host "[*] Staging all files..." -ForegroundColor Cyan
git add -A

Write-Host ("[*] Committing changes with message: '" + $CommitMessage + "'...") -ForegroundColor Cyan
git commit -m "$CommitMessage"

if ($LASTEXITCODE -ne 0) {
    Write-Host "[X] Git commit failed." -ForegroundColor Red
    exit 1
}

Write-Host "[*] Pushing to remote origin..." -ForegroundColor Cyan
git push origin HEAD

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[OK] Successfully pushed changes to GitHub!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[X] Git push failed. Please check your network or repository permissions." -ForegroundColor Red
    exit 1
}
