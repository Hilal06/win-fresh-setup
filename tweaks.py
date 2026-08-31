"""
Windows System Tweaks & Optimization Module
Applies safe registry-level tweaks for Windows 10 & 11.
"""

import sys
import os
import subprocess
from typing import List, Dict, Any, Tuple

try:
    import winreg
except ImportError:
    winreg = None

TWEAKS_LIST = [
    {
        "id": "dark_mode",
        "name": "🌙 Enable Dark Mode (System & Apps)",
        "description": "Switch Windows interface and applications to Dark Theme",
        "default": True,
        "actions": [
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", "AppsUseLightTheme", winreg.REG_DWORD if winreg else 4, 0),
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", "SystemUsesLightTheme", winreg.REG_DWORD if winreg else 4, 0)
        ]
    },
    {
        "id": "show_file_ext",
        "name": "📄 Show File Name Extensions",
        "description": "Always display file extensions (.txt, .exe, .py) in File Explorer",
        "default": True,
        "actions": [
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "HideFileExt", winreg.REG_DWORD if winreg else 4, 0)
        ]
    },
    {
        "id": "show_hidden_files",
        "name": "👁️ Show Hidden Files and Folders",
        "description": "Reveal hidden system files in File Explorer",
        "default": True,
        "actions": [
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "Hidden", winreg.REG_DWORD if winreg else 4, 1)
        ]
    },
    {
        "id": "enable_end_task",
        "name": "⚡ Enable 'End Task' on Taskbar Right-Click (Win 11)",
        "description": "Add instant End Task option when right-clicking taskbar items",
        "default": True,
        "actions": [
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\TaskbarDeveloperSettings", "TaskbarEndTask", winreg.REG_DWORD if winreg else 4, 1)
        ]
    },
    {
        "id": "disable_bing_search",
        "name": "🔍 Disable Bing Web Search in Start Menu",
        "description": "Speed up Start Menu search to only index local files and apps",
        "default": True,
        "actions": [
            ("HKCU", r"Software\Policies\Microsoft\Windows\Explorer", "DisableSearchBoxSuggestions", winreg.REG_DWORD if winreg else 4, 1),
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Search", "BingSearchEnabled", winreg.REG_DWORD if winreg else 4, 0)
        ]
    },
    {
        "id": "launch_to_this_pc",
        "name": "💻 Open File Explorer to 'This PC'",
        "description": "Opens 'This PC' with drives listed instead of Home / Quick Access",
        "default": True,
        "actions": [
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "LaunchTo", winreg.REG_DWORD if winreg else 4, 1)
        ]
    },
    {
        "id": "taskbar_align_left",
        "name": "📐 Align Taskbar to Left (Windows 11)",
        "description": "Moves the Windows 11 Start button and icons to the bottom-left corner",
        "default": False,
        "actions": [
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "TaskbarAl", winreg.REG_DWORD if winreg else 4, 0)
        ]
    }
]

def get_hkey_root(name: str):
    if not winreg:
        return None
    if name == "HKCU":
        return winreg.HKEY_CURRENT_USER
    elif name == "HKLM":
        return winreg.HKEY_LOCAL_MACHINE
    return winreg.HKEY_CURRENT_USER

def set_registry_value(hive_str: str, subkey: str, value_name: str, value_type: int, value_data: Any) -> bool:
    """Set or create a Windows registry key value."""
    if not winreg:
        return False
    try:
        root = get_hkey_root(hive_str)
        # Open or create subkey with write access
        key = winreg.CreateKeyEx(root, subkey, 0, winreg.KEY_SET_VALUE | winreg.KEY_WRITE)
        winreg.SetValueEx(key, value_name, 0, value_type, value_data)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        return False

def restart_explorer() -> bool:
    """Gracefully restart explorer.exe to apply UI changes immediately."""
    try:
        subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.Popen(["explorer.exe"])
        return True
    except Exception:
        return False

def apply_selected_tweaks(selected_tweak_ids: List[str]) -> List[Dict[str, Any]]:
    """Apply chosen tweaks by ID."""
    results = []
    for tweak in TWEAKS_LIST:
        if tweak["id"] in selected_tweak_ids:
            all_ok = True
            for hive, subkey, val_name, val_type, val_data in tweak["actions"]:
                ok = set_registry_value(hive, subkey, val_name, val_type, val_data)
                if not ok:
                    all_ok = False
            results.append({
                "name": tweak["name"],
                "success": all_ok,
                "description": tweak["description"]
            })
    return results
