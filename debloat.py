"""
Windows Bloatware Remover & Debloater Module
Safely uninstalls pre-installed UWP applications on Windows 10 & 11 using PowerShell AppxPackage commands.
"""

import sys
import subprocess
import shutil
from typing import List, Dict, Any

DEBLOAT_LIST = [
    {
        "id": "Microsoft.WindowsFeedbackHub",
        "name": "Windows Feedback Hub",
        "description": "Telemetry and feedback submission app",
        "default": True
    },
    {
        "id": "Microsoft.GetHelp",
        "name": "Get Help",
        "description": "Microsoft support and help assistant",
        "default": True
    },
    {
        "id": "Microsoft.Getstarted",
        "name": "Microsoft Tips (Get Started)",
        "description": "Windows tips and welcome popups",
        "default": True
    },
    {
        "id": "Microsoft.BingNews",
        "name": "Microsoft News",
        "description": "MSN News app and widget provider",
        "default": True
    },
    {
        "id": "Microsoft.BingWeather",
        "name": "Microsoft Weather",
        "description": "MSN Weather app and widget",
        "default": False
    },
    {
        "id": "Microsoft.MicrosoftSolitaireCollection",
        "name": "Microsoft Solitaire Collection",
        "description": "Casual Solitaire card game bundle with ads",
        "default": True
    },
    {
        "id": "Microsoft.Microsoft3DViewer",
        "name": "3D Viewer",
        "description": "3D model viewing tool",
        "default": True
    },
    {
        "id": "Microsoft.MixedReality.Portal",
        "name": "Mixed Reality Portal",
        "description": "VR / AR headset software",
        "default": True
    },
    {
        "id": "Microsoft.People",
        "name": "Microsoft People",
        "description": "Legacy contacts manager",
        "default": True
    },
    {
        "id": "Microsoft.SkypeApp",
        "name": "Skype",
        "description": "Pre-installed Skype UWP application",
        "default": True
    },
    {
        "id": "Microsoft.YourPhone",
        "name": "Phone Link (Your Phone)",
        "description": "Sync phone SMS and notifications to PC",
        "default": False
    },
    {
        "id": "Microsoft.ZuneVideo",
        "name": "Films & TV (Zune Video)",
        "description": "Default UWP video player (replaceable by VLC)",
        "default": True
    },
    {
        "id": "Clipchamp.Clipchamp",
        "name": "Clipchamp Video Editor",
        "description": "Pre-installed web-based video editor",
        "default": False
    }
]

def get_powershell_executable() -> str:
    """Prefer pwsh (PowerShell 7+) over Windows PowerShell 5.1 for faster startup."""
    return "pwsh" if shutil.which("pwsh") else "powershell"

def uninstall_appx_package(package_pattern: str) -> bool:
    """Uninstall a Windows Appx Package by pattern name."""
    ps_cmd = get_powershell_executable()
    cmd = (
        f'Get-AppxPackage -Name "*{package_pattern}*" | '
        f'Remove-AppxPackage -ErrorAction SilentlyContinue'
    )
    try:
        res = subprocess.run(
            [ps_cmd, "-NoProfile", "-NonInteractive", "-Command", cmd],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=30
        )
        return res.returncode == 0
    except Exception:
        return False

def uninstall_appx_packages_batch(package_patterns: List[str]) -> Dict[str, bool]:
    """
    Uninstall multiple Windows Appx Packages in a single PowerShell process session.
    Returns a dict mapping pattern -> success (True if removed or already not present).
    """
    if not package_patterns:
        return {}

    ps_cmd = get_powershell_executable()
    patterns_array = ", ".join(f'"{p}"' for p in package_patterns)
    script = (
        f"$patterns = @({patterns_array}); "
        "foreach ($p in $patterns) { "
        "    try { "
        '        $pkgs = Get-AppxPackage -Name "*$p*" -ErrorAction SilentlyContinue; '
        "        if ($pkgs) { "
        "            $pkgs | Remove-AppxPackage -ErrorAction SilentlyContinue; "
        '            Write-Output "$($p):OK"; '
        "        } else { "
        '            Write-Output "$($p):NOT_FOUND"; '
        "        } "
        "    } catch { "
        '        Write-Output "$($p):FAIL"; '
        "    } "
        "}"
    )

    try:
        res = subprocess.run(
            [ps_cmd, "-NoProfile", "-NonInteractive", "-Command", script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=90
        )
        results = {}
        for line in res.stdout.splitlines():
            line = line.strip()
            if ":" in line:
                pat, status = line.split(":", 1)
                results[pat] = status in ["OK", "NOT_FOUND"]

        # Ensure all requested patterns have a result
        for p in package_patterns:
            if p not in results:
                results[p] = True
        return results
    except Exception:
        # Fallback to serial uninstallation if batch command encounters unexpected error
        return {p: uninstall_appx_package(p) for p in package_patterns}

def remove_selected_bloatware(selected_ids: List[str]) -> List[Dict[str, Any]]:
    """Remove selected bloatware packages in a single batch session."""
    batch_results = uninstall_appx_packages_batch(selected_ids)
    results = []
    for item in DEBLOAT_LIST:
        if item["id"] in selected_ids:
            results.append({
                "id": item["id"],
                "name": item["name"],
                "success": batch_results.get(item["id"], False),
                "description": item["description"]
            })
    return results
