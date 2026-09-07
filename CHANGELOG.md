# Changelog 📝

All notable changes to the **win-fresh-setup** project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased] - 2026-09-07

### 🚀 Added
- **CMD to Modern PowerShell 7+ Auto-Upgrade (`run.bat`)**:
  - Automatically detects if Modern PowerShell (`pwsh.exe`) is installed when launched from CMD.
  - Automatically downloads and installs `Microsoft.PowerShell` via Winget if missing.
  - Transitions execution seamlessly to `pwsh -NoProfile -ExecutionPolicy Bypass -File run.ps1` and closes the legacy CMD prompt.
- **Pre-Menu Administrator Elevation Prompt (`installer.py`)**:
  - Added system elevation detection before the main interactive menu is displayed.
  - Renders a styled alert panel with a `[Sangat Direkomendasikan]` (Highly Recommended) advisory note.
  - Triggers native Windows UAC (`runas` via `ShellExecuteW`) to elevate and relaunch the setup in an Administrator terminal upon user approval.
- **Direct Virtual Environment Execution**:
  - Invocations of `pip` and `installer.py` now directly call `.\.venv\Scripts\python.exe`, completely removing the dependency on `Activate.ps1`.
- **In-Memory Scriptblock Execution in Bootstrap (`bootstrap.ps1`)**:
  - `bootstrap.ps1` now invokes `run.ps1` via `[scriptblock]::Create` to guarantee execution on fresh Windows installations where local file ExecutionPolicy is `Restricted`.
- **Automated Testing & Push Pipeline (`.agents/scripts/auto_push.ps1` & `.agents/auto-push.md`)**:
  - Structured `.agents/` workflow with SOP guidelines (`auto-push.md`) for AI agents.
  - Automated pre-commit verification tool located in `.agents/scripts/auto_push.ps1` that runs the test suite (`test_installer.py`), halts on failure with detailed diagnostic logs, and automatically stages, commits, and pushes upon 100% test pass.
- **Enhanced `.gitignore` Coverage**:
  - Added comprehensive ignore rules for Python environment/cache/packaging artifacts, test output, temporary migration backups (`my-setup.json`, `migration-*.json`), log files, OS artifacts, and IDE configurations.

### 🛠️ Fixed
- **Windows Store Python Execution Alias Trap**:
  - Fixed false-positive Python detection where Windows 10/11 0-byte Microsoft Store shims in `WindowsApps` caused `python -m venv` to fail or open the Microsoft Store app.
  - Replaced shallow `where python` / `Get-Command python` with real execution validation (`sys.executable` evaluation) and multi-path search (`%LOCALAPPDATA%\Programs\Python\...`, `%ProgramFiles%\Python\...`).
- **PowerShell Execution Policy Blockades**:
  - Fixed script execution failures on brand new Windows setups by adding explicit `-ExecutionPolicy Bypass -Scope Process` in bootstrap instructions and launchers.
- **Session Environment PATH Refresh**:
  - Ensured newly installed Python directories and script paths are immediately injected into the active terminal session without requiring a system reboot or shell restart.

---

## [1.0.0] - 2026-09-06

### 🚀 Initial Feature Suite
- **Interactive Checkbox TUI**: Powered by `rich` and `questionary`.
- **Live In-App Winget Search**: Search, inspect, and install packages on the fly.
- **Curated Persona Presets**: Developer, Gamer, Creator, Minimalist, Power User profiles.
- **Windows Debloater**: Uninstalls pre-loaded Windows UWP bloatware.
- **Registry Tweaks & Rollback**: Safe registry tweaks with timestamped backup and revert capabilities.
- **Shell Booster**: Modern PowerShell profile configuration with PSReadLine and Starship.
- **PC Setup Migration**: Export/Import application lists to portable JSON.
- **Pre-Flight Health Checks**: Verifies disk storage, internet connectivity, and Winget service.
