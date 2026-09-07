# Windows 11 Winget App Installer - PowerShell Launcher
$ErrorActionPreference = "Stop"
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force -ErrorAction SilentlyContinue
Set-Location $PSScriptRoot

Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "         Windows 11 Winget App Installer Setup         " -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host ""

function Get-PythonExecutable {
    # 1. Test standard 'python' in PATH (ensure it's not the Windows Store 0-byte shim)
    $py = Get-Command python -ErrorAction SilentlyContinue
    if ($py) {
        try {
            $ver = & $py.Source -c "import sys; print(sys.executable)" 2>$null
            if ($LASTEXITCODE -eq 0 -and $ver -and (Test-Path $ver)) {
                return $ver.Trim()
            }
        } catch {}
    }

    # 2. Test 'py' launcher
    $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($pyLauncher) {
        try {
            $ver = & $pyLauncher.Source -3 -c "import sys; print(sys.executable)" 2>$null
            if ($LASTEXITCODE -eq 0 -and $ver -and (Test-Path $ver)) {
                return $ver.Trim()
            }
        } catch {}
    }

    # 3. Check known standard installation directories
    $candidatePaths = [System.Collections.Generic.List[string]]::new()
    
    # Common Python versions
    @("Python313", "Python312", "Python311", "Python310") | ForEach-Object {
        $verDir = $_
        $candidatePaths.Add("$env:LOCALAPPDATA\Programs\Python\$verDir\python.exe")
        $candidatePaths.Add("$env:ProgramFiles\Python\$verDir\python.exe")
        $candidatePaths.Add("$env:ProgramFiles\$verDir\python.exe")
        $candidatePaths.Add("C:\$verDir\python.exe")
    }

    # Dynamic search in LocalAppData Programs\Python
    if (Test-Path "$env:LOCALAPPDATA\Programs\Python") {
        Get-ChildItem -Path "$env:LOCALAPPDATA\Programs\Python" -Filter "python.exe" -Recurse -Depth 2 -ErrorAction SilentlyContinue | ForEach-Object {
            $candidatePaths.Add($_.FullName)
        }
    }

    foreach ($path in $candidatePaths) {
        if ($path -and (Test-Path $path)) {
            try {
                $ver = & $path -c "import sys; print(sys.executable)" 2>$null
                if ($LASTEXITCODE -eq 0 -and $ver) {
                    return $path.Trim()
                }
            } catch {}
        }
    }

    return $null
}

# 1. Find or Install Python
$pythonExe = Get-PythonExecutable

if (-not $pythonExe) {
    Write-Host "[!] Python was not detected or is an unconfigured Windows Store shim." -ForegroundColor Yellow
    Write-Host "[*] Installing Python 3.12 automatically via Winget..." -ForegroundColor Cyan
    
    winget install Python.Python.3.12 -e --accept-package-agreements --accept-source-agreements
    
    # Refresh PATH in current session
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    $pythonExe = Get-PythonExecutable
    if (-not $pythonExe) {
        Write-Host "[X] Python installation could not be located automatically." -ForegroundColor Red
        Write-Host "    Please install Python from https://www.python.org/downloads/ (Check 'Add Python to PATH')." -ForegroundColor Red
        exit 1
    }
}

Write-Host "[✓] Using Python: $pythonExe" -ForegroundColor Green

# Add Python directory to PATH for this session
$pyDir = Split-Path -Parent $pythonExe
$pyScriptsDir = Join-Path $pyDir "Scripts"
if ($env:Path -notlike "*$pyDir*") {
    $env:Path = "$pyDir;$pyScriptsDir;$env:Path"
}

# 2. Setup Virtual Environment
$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

if (Test-Path ".venv") {
    if (-not (Test-Path $venvPython)) {
        Write-Host "[!] Existing .venv appears corrupted. Rebuilding..." -ForegroundColor Yellow
        Remove-Item -Path ".venv" -Recurse -Force -ErrorAction SilentlyContinue
    }
}

if (-not (Test-Path ".venv")) {
    Write-Host "[*] Creating Python virtual environment (.venv)..." -ForegroundColor Cyan
    & $pythonExe -m venv .venv
}

$activePython = if (Test-Path $venvPython) { $venvPython } else { $pythonExe }

# 3. Install requirements
Write-Host "[*] Installing / Verifying requirements..." -ForegroundColor Cyan
& $activePython -m pip install --quiet --upgrade pip
& $activePython -m pip install --quiet -r requirements.txt

# 4. Run installer
Write-Host "[*] Starting TUI Installer..." -ForegroundColor Green
Write-Host ""
& $activePython installer.py

