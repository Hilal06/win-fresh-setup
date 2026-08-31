"""
Windows System Tweaks & Optimization Module
Applies safe registry-level tweaks with automatic backup & rollback for Windows 10 & 11.
"""

import sys
import os
import json
import subprocess
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional

try:
    import winreg
except ImportError:
    winreg = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
LATEST_BACKUP_FILE = os.path.join(LOGS_DIR, "latest_tweaks_backup.json")

TWEAKS_LIST = [
    {
        "id": "classic_context_menu",
        "name": "📋 Restore Classic Right-Click Context Menu (Win 11)",
        "description": "Brings back the Windows 10 full right-click context menu without 'Show more options'",
        "default": True,
        "actions": [
            ("HKCU", r"Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32", "", winreg.REG_SZ if winreg else 1, "")
        ],
        "revert_actions": [
            ("DELETE_KEY", "HKCU", r"Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}")
        ]
    },
    {
        "id": "dark_mode",
        "name": "🌙 Enable Dark Mode (System & Apps)",
        "description": "Switch Windows interface and applications to Dark Theme",
        "default": True,
        "actions": [
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", "AppsUseLightTheme", winreg.REG_DWORD if winreg else 4, 0),
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", "SystemUsesLightTheme", winreg.REG_DWORD if winreg else 4, 0)
        ],
        "revert_actions": [
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", "AppsUseLightTheme", winreg.REG_DWORD if winreg else 4, 1),
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", "SystemUsesLightTheme", winreg.REG_DWORD if winreg else 4, 1)
        ]
    },
    {
        "id": "show_file_ext",
        "name": "📄 Show File Name Extensions",
        "description": "Always display file extensions (.txt, .exe, .py) in File Explorer",
        "default": True,
        "actions": [
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "HideFileExt", winreg.REG_DWORD if winreg else 4, 0)
        ],
        "revert_actions": [
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "HideFileExt", winreg.REG_DWORD if winreg else 4, 1)
        ]
    },
    {
        "id": "show_hidden_files",
        "name": "👁️ Show Hidden Files and Folders",
        "description": "Reveal hidden system files in File Explorer",
        "default": True,
        "actions": [
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "Hidden", winreg.REG_DWORD if winreg else 4, 1)
        ],
        "revert_actions": [
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "Hidden", winreg.REG_DWORD if winreg else 4, 2)
        ]
    },
    {
        "id": "enable_end_task",
        "name": "⚡ Enable 'End Task' on Taskbar Right-Click (Win 11)",
        "description": "Add instant End Task option when right-clicking taskbar items",
        "default": True,
        "actions": [
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\TaskbarDeveloperSettings", "TaskbarEndTask", winreg.REG_DWORD if winreg else 4, 1)
        ],
        "revert_actions": [
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\TaskbarDeveloperSettings", "TaskbarEndTask", winreg.REG_DWORD if winreg else 4, 0)
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
        ],
        "revert_actions": [
            ("HKCU", r"Software\Policies\Microsoft\Windows\Explorer", "DisableSearchBoxSuggestions", winreg.REG_DWORD if winreg else 4, 0),
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Search", "BingSearchEnabled", winreg.REG_DWORD if winreg else 4, 1)
        ]
    },
    {
        "id": "launch_to_this_pc",
        "name": "💻 Open File Explorer to 'This PC'",
        "description": "Opens 'This PC' with drives listed instead of Home / Quick Access",
        "default": True,
        "actions": [
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "LaunchTo", winreg.REG_DWORD if winreg else 4, 1)
        ],
        "revert_actions": [
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "LaunchTo", winreg.REG_DWORD if winreg else 4, 2)
        ]
    },
    {
        "id": "disable_sticky_keys",
        "name": "⌨️ Disable Sticky Keys Shortcut Popup",
        "description": "Prevents the annoying Sticky Keys dialog from popping up when pressing Shift 5 times",
        "default": True,
        "actions": [
            ("HKCU", r"Control Panel\Accessibility\StickyKeys", "Flags", winreg.REG_SZ if winreg else 1, "506"),
            ("HKCU", r"Control Panel\Accessibility\Keyboard Response", "Flags", winreg.REG_SZ if winreg else 1, "122"),
            ("HKCU", r"Control Panel\Accessibility\ToggleKeys", "Flags", winreg.REG_SZ if winreg else 1, "58")
        ],
        "revert_actions": [
            ("HKCU", r"Control Panel\Accessibility\StickyKeys", "Flags", winreg.REG_SZ if winreg else 1, "510")
        ]
    },
    {
        "id": "taskbar_align_left",
        "name": "📐 Align Taskbar to Left (Windows 11)",
        "description": "Moves the Windows 11 Start button and icons to the bottom-left corner",
        "default": False,
        "actions": [
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "TaskbarAl", winreg.REG_DWORD if winreg else 4, 0)
        ],
        "revert_actions": [
            ("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "TaskbarAl", winreg.REG_DWORD if winreg else 4, 1)
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

def get_registry_value(hive_str: str, subkey: str, value_name: str) -> Tuple[bool, Any, int]:
    """Read a registry value if it exists."""
    if not winreg:
        return False, None, 0
    try:
        root = get_hkey_root(hive_str)
        key = winreg.OpenKey(root, subkey, 0, winreg.KEY_READ)
        val, vtype = winreg.QueryValueEx(key, value_name)
        winreg.CloseKey(key)
        return True, val, vtype
    except Exception:
        return False, None, 0

def set_registry_value(hive_str: str, subkey: str, value_name: str, value_type: int, value_data: Any) -> bool:
    """Set or create a Windows registry key value."""
    if not winreg:
        return False
    try:
        root = get_hkey_root(hive_str)
        key = winreg.CreateKeyEx(root, subkey, 0, winreg.KEY_SET_VALUE | winreg.KEY_WRITE)
        winreg.SetValueEx(key, value_name, 0, value_type, value_data)
        winreg.CloseKey(key)
        return True
    except Exception:
        return False

def delete_registry_key_tree(hive_str: str, subkey: str) -> bool:
    """Recursively delete a registry key."""
    if not winreg:
        return False
    try:
        root = get_hkey_root(hive_str)
        # Using reg.exe command for safe recursive deletion
        root_name = "HKCU" if hive_str == "HKCU" else "HKLM"
        full_path = f"{root_name}\\{subkey}"
        subprocess.run(["reg", "delete", full_path, "/f"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False

def backup_current_tweaks(selected_tweak_ids: List[str]) -> Optional[str]:
    """Back up current registry states before applying tweaks."""
    if not winreg:
        return None
    backup_data = {}
    for tweak in TWEAKS_LIST:
        if tweak["id"] in selected_tweak_ids:
            tweak_backup = []
            for action in tweak["actions"]:
                hive, subkey, val_name, _, _ = action
                exists, val, vtype = get_registry_value(hive, subkey, val_name)
                tweak_backup.append({
                    "hive": hive,
                    "subkey": subkey,
                    "val_name": val_name,
                    "exists": exists,
                    "val": val,
                    "vtype": vtype
                })
            backup_data[tweak["id"]] = tweak_backup

    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(LOGS_DIR, f"tweaks_backup_{timestamp}.json")
    try:
        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(backup_data, f, indent=2)
        with open(LATEST_BACKUP_FILE, "w", encoding="utf-8") as f:
            json.dump(backup_data, f, indent=2)
        return backup_file
    except Exception:
        return None

def restart_explorer() -> bool:
    """Gracefully restart explorer.exe to apply UI changes immediately."""
    try:
        subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.Popen(["explorer.exe"])
        return True
    except Exception:
        return False

def apply_selected_tweaks(selected_tweak_ids: List[str]) -> List[Dict[str, Any]]:
    """Apply chosen tweaks by ID with auto-backup."""
    backup_current_tweaks(selected_tweak_ids)
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

def revert_selected_tweaks(selected_tweak_ids: List[str]) -> List[Dict[str, Any]]:
    """Revert chosen tweaks back to default / previous state."""
    results = []
    # Check if latest backup file exists
    backup_data = {}
    if os.path.exists(LATEST_BACKUP_FILE):
        try:
            with open(LATEST_BACKUP_FILE, "r", encoding="utf-8") as f:
                backup_data = json.load(f)
        except Exception:
            backup_data = {}

    for tweak in TWEAKS_LIST:
        if tweak["id"] in selected_tweak_ids:
            all_ok = True
            # First try restoring from exact backup if found
            if tweak["id"] in backup_data:
                for item in backup_data[tweak["id"]]:
                    if item.get("exists"):
                        ok = set_registry_value(item["hive"], item["subkey"], item["val_name"], item["vtype"], item["val"])
                        if not ok:
                            all_ok = False
                    else:
                        # Value didn't exist before, attempt to delete/clean
                        if "revert_actions" in tweak:
                            for rev in tweak["revert_actions"]:
                                if rev[0] == "DELETE_KEY":
                                    delete_registry_key_tree(rev[1], rev[2])
            elif "revert_actions" in tweak:
                for rev in tweak["revert_actions"]:
                    if rev[0] == "DELETE_KEY":
                        delete_registry_key_tree(rev[1], rev[2])
                    else:
                        hive, subkey, val_name, val_type, val_data = rev
                        set_registry_value(hive, subkey, val_name, val_type, val_data)

            results.append({
                "name": tweak["name"],
                "success": all_ok,
                "description": tweak["description"]
            })
    return results
