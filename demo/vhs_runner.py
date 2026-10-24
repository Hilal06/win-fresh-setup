#!/usr/bin/env python3
"""
vhs_runner.py - Standalone VHS & Showcase Recording Runner for win-fresh-setup.
Runs the exact production TUI from installer.py in a safe, headless-ready environment
without requiring UAC prompts or performing actual package installations.
"""

import sys
import os
import time

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Add repository root to Python path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import installer
import tweaks
import debloat
from rich.panel import Panel

# 1. Simulate Elevated Administrator Session in memory (no UAC prompt pop-up)
installer.is_admin = lambda: True

# 2. Instant pre-cached installed applications for realistic badge rendering
MOCK_INSTALLED = {
    "mozilla.firefox",
    "google.chrome",
    "git.git",
    "openjs.nodejs.lts"
}
installer.scan_installed_apps = lambda force_refresh=False, show_spinner=False: set(MOCK_INSTALLED)

# 3. Simulated realistic Winget installation queue with live progress
def simulated_winget_install(app, log_file_path):
    """Simulate rapid visual installation for recording demos."""
    time.sleep(0.6)
    with open(log_file_path, "a", encoding="utf-8") as f:
        f.write(f"Simulated install for {app['name']} ({app['id']})\n")
    return {"status": "SUCCESS", "message": "Installed successfully"}

installer.run_winget_install = simulated_winget_install

if __name__ == "__main__":
    installer.ensure_dirs()
    
    if len(sys.argv) > 2 and sys.argv[1] == "--screen":
        screen = sys.argv[2]
        apps = installer.load_apps()
        installed_set = set(MOCK_INSTALLED)
        
        if screen == "elevation":
            installer.is_admin = lambda: False
            installer.print_banner()
            installer.CONSOLE.print(
                Panel(
                    "[bold yellow][!] Hak Akses Administrator Diwajibkan[/bold yellow]\n\n"
                    "Installer saat ini berjalan sebagai [bold cyan]Standard User[/bold cyan].\n\n"
                    "Fitur seperti instalasi paket, registry tweaks, debloater, dan shell booster "
                    "memerlukan hak akses [bold green]Administrator[/bold green] penuh agar dapat bekerja optimal.\n\n"
                    "[bold cyan][*] Membuka sesi Administrator via UAC... Silakan klik 'Yes' pada jendela konfirmasi.[/bold cyan]",
                    title="[bold yellow]Auto-Elevation[/bold yellow]",
                    border_style="yellow",
                    padding=(1, 2)
                )
            )
            installer.CONSOLE.print("\n[bold cyan][*] Membuka jendela Administrator baru...[/bold cyan]")
            installer.CONSOLE.print("[dim]Prompt UAC Windows terpicu secara otomatis. Sesi non-administrator akan ditutup setelah elevasi disetujui.[/dim]")
            time.sleep(60)
            sys.exit(0)

        elif screen == "select_apps":
            installer.print_banner()
            choices = installer.build_choices(apps, installed_set=installed_set)
            instruction_text = "(Space to select/deselect, 'a' to toggle all, 'i' to invert, Enter to confirm)"
            installer.questionary.checkbox(
                "Select applications to install:",
                choices=choices,
                instruction=instruction_text,
                style=installer.CUSTOM_STYLE
            ).ask()
            sys.exit(0)

        elif screen == "presets":
            installer.handle_presets_menu(apps, installed_set)
            sys.exit(0)

        elif screen == "debloat":
            installer.handle_debloat_menu()
            sys.exit(0)

        elif screen == "tweaks":
            installer.print_banner()
            installer.CONSOLE.print("[bold cyan]=== System & Explorer Tweaks ===[/bold cyan]\n")
            tweak_choices = []
            for t in tweaks.TWEAKS_LIST:
                display_title = f"{t['name']} - [dim]{t['description']}[/dim]"
                tweak_choices.append(installer.Choice(
                    title=display_title,
                    value=t["id"],
                    checked=t.get("default", False)
                ))
            installer.questionary.checkbox(
                "Select Tweaks to apply to Windows:",
                choices=tweak_choices,
                instruction="(Space: toggle, Enter: apply, Ctrl+C: back)",
                style=installer.CUSTOM_STYLE
            ).ask()
            sys.exit(0)

        elif screen == "shell_booster":
            installer.handle_shell_booster_menu()
            sys.exit(0)

        elif screen == "preflight":
            installer.handle_preflight_check()
            sys.exit(0)

    installer.main_menu()
