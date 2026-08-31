"""
PowerShell & Terminal Booster Module
Configures modern PowerShell profile, PSReadLine Predictive IntelliSense, Starship, and aliases.
"""

import os
import sys
import subprocess
from typing import Dict, Any, List

def get_powershell_profile_paths() -> List[str]:
    """Get candidate PowerShell profile paths."""
    user_home = os.path.expanduser("~")
    paths = [
        os.path.join(user_home, "Documents", "PowerShell", "Microsoft.PowerShell_profile.ps1"),
        os.path.join(user_home, "Documents", "WindowsPowerShell", "Microsoft.PowerShell_profile.ps1")
    ]
    return paths

MODERN_PROFILE_CONTENT = """# ========================================================
# win-fresh-setup - Modern PowerShell Profile
# ========================================================

# 1. Force UTF-8 Encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# 2. PSReadLine Predictive IntelliSense (Fish-shell style auto-suggestions)
if (Get-Module -ListAvailable -Name PSReadLine) {
    Import-Module PSReadLine
    Set-PSReadLineOption -PredictionSource HistoryAndPlugin -ErrorAction SilentlyContinue
    Set-PSReadLineOption -PredictionViewStyle ListView -ErrorAction SilentlyContinue
    Set-PSReadLineOption -EditMode Windows -ErrorAction SilentlyContinue
    Set-PSReadLineKeyHandler -Key Tab -Function Complete -ErrorAction SilentlyContinue
}

# 3. Initialize Starship Prompt (if installed)
if (Get-Command starship -ErrorAction SilentlyContinue) {
    Invoke-Expression (&starship init powershell)
}

# 4. Handy Power-User Aliases & Functions
function which ($name) { Get-Command $name -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source }
function touch ($file) { New-Item -ItemType File -Path $file -Force | Out-Null }
function reload-profile { & $PROFILE }

Set-Alias -Name ll -Value Get-ChildItem -Option AllScope -ErrorAction SilentlyContinue
Set-Alias -Name grep -Value Select-String -Option AllScope -ErrorAction SilentlyContinue
"""

def setup_powershell_profile() -> Dict[str, Any]:
    """Apply the optimized PowerShell profile."""
    configured_paths = []
    errors = []
    
    for path in get_powershell_profile_paths():
        try:
            folder = os.path.dirname(path)
            if not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(MODERN_PROFILE_CONTENT)
            configured_paths.append(path)
        except Exception as e:
            errors.append(f"{path}: {e}")
            
    return {
        "success": len(configured_paths) > 0,
        "configured_paths": configured_paths,
        "errors": errors
    }
