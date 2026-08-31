# win-fresh-setup 🚀

[![CI Validation](https://github.com/Hilal06/win-fresh-setup/actions/workflows/ci.yml/badge.svg)](https://github.com/Hilal06/win-fresh-setup/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An interactive Terminal User Interface (TUI) and automated package installer to batch-install software and apply system optimizations on fresh Windows 11 & 10 setups using **Winget (Windows Package Manager)**.

---

## ⚡ Quick 1-Line Online Bootstrap (No Git Required)

Open PowerShell as Administrator and run:
```powershell
irm https://raw.githubusercontent.com/Hilal06/win-fresh-setup/main/bootstrap.ps1 | iex
```
This automatically downloads the repository, prepares the Python virtual environment, and launches the interactive installer immediately.

---

## ✨ Features

- **⚡ 1-Line Web Bootstrap**: Run a single PowerShell command on a completely fresh Windows install without manually downloading files or installing Git first.
- **🎯 Curated Preset Profiles**: Instant 1-click profiles for **Developer**, **Gamer**, **Content Creator**, **Minimalist**, and **Power User**.
- **🛠️ Windows 10/11 System Tweaks**: Apply safe registry-level tweaks (Dark Mode, Show File Extensions, Enable 'End Task' in Taskbar, Disable Bing Search, etc.).
- **🎨 Interactive TUI Checkboxes**: Check / uncheck applications using keyboard navigation.
  - `Space`: Toggle selected / unselected
  - `a`: Select / Deselect All
  - `i`: Invert selection
  - `Enter`: Confirm selection
- **📁 Easily Editable `apps.json`**: Manage your custom list of software, categories, Winget IDs, and default checked states.
- **📂 Category Filtering**: Install by specific software categories (e.g. *Web Browsers*, *Developer Tools*, *Media & Audio*, *System & Customization*).
- **➕ Interactive App Addition**: Add new applications directly from the TUI or by editing `apps.json`.
- **⚡ Live Installation Progress**: Real-time progress bar, spinner, status updates, and summary table (Success, Already Installed, Failed).
- **📜 Detailed Logging**: All installation logs are saved automatically to `logs/winget_install_<timestamp>.log`.
- **🚀 One-Click Launchers**: `run.bat` and `run.ps1` automatically detect and install Python & dependencies if missing.

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

### Method 1: Double-Click `run.bat` (Recommended)
Simply double-click [run.bat](file:///D:/Workspace/Script/run.bat). It will:
1. Check if Python is installed (if not, auto-installs Python 3.12 via Winget).
2. Set up a local Python virtual environment `.venv`.
3. Install dependencies (`questionary`, `rich`, `colorama`).
4. Launch the TUI installer.

---

### Method 2: Run via PowerShell
Right-click [run.ps1](file:///D:/Workspace/Script/run.ps1) and choose **Run with PowerShell**, or in terminal:
```powershell
.\run.ps1
```

---

### Method 3: Manual Python Execution
If you already have Python and virtual environment configured:
```bash
pip install -r requirements.txt
python installer.py
```

---

## ✏️ How to Add / Edit Apps

### Option A: Edit [apps.json](file:///D:/Workspace/Script/apps.json)
You can open and edit `apps.json` directly. Each entry follows this format:
```json
{
  "category": "Developer Tools",
  "name": "Node.js (LTS)",
  "id": "OpenJS.NodeJS.LTS",
  "description": "JavaScript runtime built on Chrome V8 engine",
  "default": true
}
```

### Option B: Add App directly from TUI
Select **`➕ Add New App to apps.json`** in the main menu to interactively add any package.

---

## 🧪 Automated Testing
Run the built-in test suite:
```powershell
.\.venv\Scripts\python.exe test_installer.py
```

---

## 👤 Author & Credits

* **Author / Creator:** [Hilal06](https://github.com/Hilal06)
* **Repository:** [win-fresh-setup](https://github.com/Hilal06/win-fresh-setup)
* **License:** MIT License
