"""
Windows Bloatware Remover & Debloater Module
Safely uninstalls pre-installed UWP applications on Windows 10 & 11 using PowerShell AppxPackage commands.
"""

import sys
import subprocess
from typing import List, Dict, Any

DEBLOAT_LIST = [
    {
        "id": "Microsoft.WindowsFeedbackHub",
        "name": "📢 Windows Feedback Hub",
        "description": "Telemetry and feedback submission app",
        "default": True
    },
    {
        "id": "Microsoft.GetHelp",
        "name": "❓ Get Help",
        "description": "Microsoft support and help assistant",
        "default": True
    },
    {
        "id": "Microsoft.Getstarted",
        "name": "💡 Microsoft Tips (Get Started)",
        "description": "Windows tips and welcome popups",
        "default": True
    },
    {
        "id": "Microsoft.BingNews",
        "name": "📰 Microsoft News",
        "description": "MSN News app and widget provider",
        "default": True
    },
    {
        "id": "Microsoft.BingWeather",
        "name": "⛅ Microsoft Weather",
        "description": "MSN Weather app and widget",
        "default": False
    },
    {
        "id": "Microsoft.MicrosoftSolitaireCollection",
        "name": "🃏 Microsoft Solitaire Collection",
        "description": "Casual Solitaire card game bundle with ads",
        "default": True
    },
    {
        "id": "Microsoft.Microsoft3DViewer",
        "name": "🧊 3D Viewer",
        "description": "3D model viewing tool",
        "default": True
    },
    {
        "id": "Microsoft.MixedReality.Portal",
        "name": "🥽 Mixed Reality Portal",
        "description": "VR / AR headset software",
        "default": True
    },
    {
        "id": "Microsoft.People",
        "name": "👥 Microsoft People",
        "description": "Legacy contacts manager",
        "default": True
    },
    {
        "id": "Microsoft.SkypeApp",
        "name": "💬 Skype",
        "description": "Pre-installed Skype UWP application",
        "default": True
    },
    {
        "id": "Microsoft.YourPhone",
        "name": "📱 Phone Link (Your Phone)",
        "description": "Sync phone SMS and notifications to PC",
        "default": False
    },
    {
        "id": "Microsoft.ZuneVideo",
        "name": "🎬 Films & TV (Zune Video)",
        "description": "Default UWP video player (replaceable by VLC)",
        "default": True
    },
    {
        "id": "Clipchamp.Clipchamp",
        "name": "🎞️ Clipchamp Video Editor",
        "description": "Pre-installed web-based video editor",
        "default": False
    }
]

def uninstall_appx_package(package_pattern: str) -> bool:
    """Uninstall a Windows Appx Package by pattern name."""
    cmd = (
        f'Get-AppxPackage -Name "*{package_pattern}*" | '
        f'Remove-AppxPackage -ErrorAction SilentlyContinue'
    )
    try:
        res = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=30
        )
        return res.returncode == 0
    except Exception:
        return False

def remove_selected_bloatware(selected_ids: List[str]) -> List[Dict[str, Any]]:
    """Remove selected bloatware packages."""
    results = []
    for item in DEBLOAT_LIST:
        if item["id"] in selected_ids:
            success = uninstall_appx_package(item["id"])
            results.append({
                "id": item["id"],
                "name": item["name"],
                "success": success,
                "description": item["description"]
            })
    return results
