# win-fresh-setup 🚀

[![CI Validation](https://github.com/Hilal06/win-fresh-setup/actions/workflows/ci.yml/badge.svg)](https://github.com/Hilal06/win-fresh-setup/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An interactive Terminal User Interface (TUI) and automated package installer to batch-install software, remove bloatware, and apply system optimizations on fresh Windows 11 & 10 setups using **Winget (Windows Package Manager)**.

---

## ⚡ Quick 1-Line Online Bootstrap (No Git Required)

Open PowerShell as Administrator and run:
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; irm https://raw.githubusercontent.com/Hilal06/win-fresh-setup/main/bootstrap.ps1 | iex
```
*✨ Automatically downloads the repository, prepares the Python environment, launches the interactive installer, and cleans up all temporary setup files upon exit!*

---

## ✨ Features

- **⚡ 1-Line Web Bootstrap**: Run a single PowerShell command on a completely fresh Windows install without downloading files or installing Git first.
- **🛡️ Pre-Flight Administrator Elevation Check**: Automatically prompts non-admin users to elevate via native Windows UAC (`runas`) before entering the main menu with a "Sangat Direkomendasikan" notice.
- **🔄 CMD to Modern PowerShell 7+ Auto-Upgrade**: Launching `run.bat` from CMD detects missing PowerShell 7, installs `Microsoft.PowerShell` via Winget, and seamlessly transitions execution to `pwsh`.
- **🐍 Robust Python & Virtual Environment Engine**: Auto-detects real Python installations (bypassing the Windows Store 0-byte execution alias trap), injects session PATH, and runs directly via `.venv` binaries.
- **🔍 Live In-App Winget Search**: Search for any software in the Winget catalog directly inside the TUI and install or save it immediately.
- **🧹 Windows Bloatware Remover (Debloater)**: Safely uninstall pre-installed Windows UWP apps (Feedback Hub, 3D Viewer, Solitaire, News, Tips, etc.).
- **💾 PC Setup Migration & Backup**: Export your installed application inventory to a portable `my-setup.json` file and import it on any new PC.
- **📊 Interactive Upgrade Dashboard**: View installed vs latest available software versions in a styled table with selective / bulk upgrade controls.
- **🎯 Curated Preset Profiles**: Instant 1-click profiles for **Developer**, **Gamer**, **Content Creator**, **Minimalist**, and **Power User**.
- **🛠️ Windows 10/11 Tweaks with Rollback**: Apply safe registry tweaks (Classic Context Menu, Dark Mode, Show File Extensions, Taskbar End Task, Disable Bing Search) with automatic backup and 1-click rollback.
- **⚡ Terminal & PowerShell Quick-Booster**: Automatically configures PowerShell with **PSReadLine Predictive IntelliSense** (Fish-shell style autocomplete), **Starship prompt**, and power-user aliases (`ll`, `grep`, `which`, `touch`).
- **🩺 Pre-Flight System Health & Disk Space Check**: Live check for `C:\` drive storage, administrator privileges, internet connection, and Winget CDN service.
- **🎨 Interactive TUI Checkboxes**: Check / uncheck applications using keyboard navigation.
  - `Space`: Toggle selected / unselected
  - `a`: Select / Deselect All
  - `i`: Invert selection
  - `Enter`: Confirm selection
- **📁 Editable `apps.json`**: Manage your custom list of software, categories, Winget IDs, and default checked states.
- **📜 Detailed Logging**: All installation logs are saved automatically to `logs/winget_install_<timestamp>.log`.

---

## 📦 Default Included Applications (34 Apps)

| Application | Winget Package ID | Category |
|---|---|---|
| **Mozilla Firefox** | `Mozilla.Firefox` | Web Browsers |
| **Google Chrome** | `Google.Chrome` | Web Browsers |
| **Brave Browser** | `Brave.Brave` | Web Browsers |
| **VLC Media Player** | `VideoLAN.VLC` | Media & Audio |
| **FxSound** | `FxSound.FxSound` | Media & Audio |
| **Spotify** | `Spotify.Spotify` | Media & Audio |
| **OBS Studio** | `OBSProject.OBSStudio` | Media & Audio |
| **PDFgear** | `PDFgear.PDFgear` | Productivity & Documents |
| **Notepad++** | `Notepad++.Notepad++` | Productivity & Documents |
| **7-Zip** | `7zip.7zip` | Productivity & Documents |
| **Obsidian** | `Obsidian.Obsidian` | Productivity & Documents |
| **Discord** | `Discord.Discord` | Communication & Social |
| **WhatsApp** | `9NKSQGP7F2NH` | Communication & Social |
| **Telegram** | `Telegram.TelegramDesktop` | Communication & Social |
| **Quick Share (Google)** | `Google.QuickShare` | File Sharing & Remote Access |
| **LocalSend** | `LocalSend.LocalSend` | File Sharing & Remote Access |
| **RustDesk** | `RustDesk.RustDesk` | File Sharing & Remote Access |
| **Tailscale** | `Tailscale.Tailscale` | File Sharing & Remote Access |
| **Visual Studio Code** | `Microsoft.VisualStudioCode` | Developer Tools |
| **Windows Terminal** | `Microsoft.WindowsTerminal` | Developer Tools |
| **PowerShell** | `Microsoft.PowerShell` | Developer Tools |
| **Starship** | `Starship.Starship` | Developer Tools |
| **Node.js (LTS)** | `OpenJS.NodeJS.LTS` | Developer Tools |
| **Git** | `Git.Git` | Developer Tools |
| **Arduino IDE** | `ArduinoSA.IDE.stable` | Developer Tools |
| **Steam** | `Valve.Steam` | Gaming & Peripherals |
| **NVIDIA App** | `XP8CLZL93F5Z4P` | Gaming & Peripherals |
| **DS4Windows** | `Ryochan7.DS4Windows` | Gaming & Peripherals |
| **UniGetUI** | `Devolutions.UniGetUI` | System & Customization |
| **Bulk Crap Uninstaller** | `Klocman.BulkCrapUninstaller` | System & Customization |
| **Winaero Tweaker** | `winaero.tweaker` | System & Customization |
| **Windhawk** | `RamenSoftware.Windhawk` | System & Customization |
| **Wise Disk Cleaner** | `WiseCleaner.WiseDiskCleaner` | System & Customization |
| **PowerToys** | `Microsoft.PowerToys` | System & Customization |

---

## 🚀 How to Run Locally

### Method 1: Double-Click `run.bat` (Recommended - No Policy Restrictions)
Simply double-click [run.bat](file:///D:/Workspace/Script/run.bat). It will:
1. Auto-detect and install modern PowerShell 7 (`pwsh`) if missing, then switch session.
2. Check if Python is installed (if not, auto-installs Python 3.12 via Winget).
3. Set up a local Python virtual environment `.venv`.
4. Install dependencies (`questionary`, `rich`).
5. Launch the TUI installer.

---

### Method 2: Run via PowerShell
In PowerShell terminal:
```powershell
powershell -ExecutionPolicy Bypass -File .\run.ps1
```

---

### Method 3: Manual Python Execution
If you already have Python and virtual environment configured:
```bash
pip install -r requirements.txt
python installer.py
```

---

## 🧪 Automated Testing & Push Automation

### Run Unit Tests
Run the built-in test suite (11 test suites):
```powershell
.\.venv\Scripts\python.exe test_installer.py
```

### Automated Test & Push Tool
Run automated test-driven commit and push:
```powershell
.\auto_push.ps1 -CommitMessage "feat: your commit message"
```
*Guarantees zero broken commits: validates all 11 test suites first; halts and displays error logs if tests fail; commits and pushes to origin upon 100% test pass.*

---

## 📋 Changelog (Dev Summary)

See full details in [CHANGELOG.md](file:///D:/Workspace/Script/CHANGELOG.md).

```text
[v1.1.0-dev] - 2026-09-07
  + Added: CMD -> PowerShell 7 (pwsh) auto-install & execution switch in run.bat
  + Added: UAC elevation prompt (runas) before main menu with "[Sangat Direkomendasikan]" notice
  + Added: Direct venv execution (.venv\Scripts\python.exe) bypassing Activate.ps1 execution policies
  + Added: In-memory scriptblock invocation in bootstrap.ps1 for restricted environments
  + Added: auto_push.ps1 automated test verification & git push tool
  * Fixed: WindowsApps/python.exe Microsoft Store false-positive execution alias trap
  * Fixed: Session PATH refresh after Winget Python installation
```

---

## 👤 Author & Credits

* **Author / Creator:** [Hilal06](https://github.com/Hilal06)
* **Repository:** [win-fresh-setup](https://github.com/Hilal06/win-fresh-setup)
* **License:** MIT License
