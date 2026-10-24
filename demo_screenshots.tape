# VHS Tape for Real In-App Screenshots
Set Shell "pwsh"
Set FontSize 14
Set Width 1280
Set Height 820
Set Padding 16
Set WindowBar Colorful
Set Margin 20
Set Theme "Catppuccin Mocha"

# 1. UAC Elevation Prompt
Type ".\.venv\Scripts\python.exe demo/vhs_runner.py --screen elevation"
Enter
Sleep 2s
Screenshot "demo/01_elevation_prompt.png"
Ctrl+C
Sleep 500ms
Type "Clear-Host"
Enter
Sleep 500ms

# 2. Main Navigation Menu
Type ".\.venv\Scripts\python.exe demo/vhs_runner.py"
Enter
Sleep 2.5s
Screenshot "demo/02_main_menu.png"
Ctrl+C
Sleep 500ms
Type "Clear-Host"
Enter
Sleep 500ms

# 3. Batch Application Selector (Checkbox TUI)
Type ".\.venv\Scripts\python.exe demo/vhs_runner.py --screen select_apps"
Enter
Sleep 2.5s
Down 1
Sleep 400ms
Space 1
Sleep 400ms
Down 1
Sleep 400ms
Space 1
Sleep 800ms
Screenshot "demo/03_select_install_apps.png"
Ctrl+C
Sleep 500ms
Type "Clear-Host"
Enter
Sleep 500ms

# 4. Persona Presets Menu
Type ".\.venv\Scripts\python.exe demo/vhs_runner.py --screen presets"
Enter
Sleep 2.5s
Screenshot "demo/04_persona_presets.png"
Ctrl+C
Sleep 500ms
Type "Clear-Host"
Enter
Sleep 500ms

# 5. Windows Debloater (UWP Remover)
Type ".\.venv\Scripts\python.exe demo/vhs_runner.py --screen debloat"
Enter
Sleep 2.5s
Screenshot "demo/05_debloater.png"
Ctrl+C
Sleep 500ms
Type "Clear-Host"
Enter
Sleep 500ms

# 6. System & Explorer Tweaks
Type ".\.venv\Scripts\python.exe demo/vhs_runner.py --screen tweaks"
Enter
Sleep 2.5s
Screenshot "demo/06_system_tweaks.png"
Ctrl+C
Sleep 500ms
Type "Clear-Host"
Enter
Sleep 500ms

# 7. Terminal & PowerShell Booster
Type ".\.venv\Scripts\python.exe demo/vhs_runner.py --screen shell_booster"
Enter
Sleep 2.5s
Screenshot "demo/07_shell_booster.png"
Ctrl+C
Sleep 500ms
Type "Clear-Host"
Enter
Sleep 500ms

# 8. Pre-Flight System Check
Type ".\.venv\Scripts\python.exe demo/vhs_runner.py --screen preflight"
Enter
Sleep 2.5s
Screenshot "demo/08_preflight_health.png"
Ctrl+C
Sleep 500ms
Type "exit"
Enter
Sleep 1s
