import os
import sys
import io
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.text import Text

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Import internal modules
import installer
import tweaks
import debloat
import shell_booster
import json

DEMO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo")
os.makedirs(DEMO_DIR, exist_ok=True)

apps_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apps.json")
with open(apps_file, "r", encoding="utf-8") as f:
    apps_data = json.load(f)

presets_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "presets.json")
with open(presets_file, "r", encoding="utf-8") as f:
    presets_data = json.load(f)

def render_to_svg(filename: str, render_callback, width=120):
    buf = io.StringIO()
    console = Console(record=True, width=width, file=buf, force_terminal=True, color_system="truecolor")
    render_callback(console)
    svg_path = os.path.join(DEMO_DIR, filename)
    console.save_svg(svg_path, title=filename.replace(".svg", ""))
    return svg_path

def draw_banner(c: Console, is_admin: bool = True):
    admin_status = "[bold green][admin][/bold green]" if is_admin else "[dim yellow][user][/dim yellow]"
    title_art = installer.load_title()
    banner_content = (
        f"[bold #ff8800]{title_art}[/bold #ff8800]\n\n"
        f"[bold cyan]win-fresh-setup[/bold cyan]  {admin_status}\n"
        f"[dim]Windows 10 & 11 Automated Package & System Setup Suite[/dim]\n"
        f"[dim]github.com/Hilal06/win-fresh-setup[/dim]"
    )
    c.print(Align.center(Panel(Align.center(banner_content), border_style="cyan", expand=False)))

# 1. Main Banner & Mandatory Elevation Screen (Auto-Elevation)
def draw_elevation_screen(c: Console):
    draw_banner(c, is_admin=False)
    c.print("")
    c.print(Panel(
        "[bold yellow][!] Hak Akses Administrator Diwajibkan[/bold yellow]\n\n"
        "Installer saat ini berjalan sebagai [bold cyan]Standard User[/bold cyan].\n\n"
        "Fitur seperti instalasi paket, registry tweaks, debloater, dan shell booster "
        "memerlukan hak akses [bold green]Administrator[/bold green] penuh agar dapat bekerja optimal.\n\n"
        "[bold cyan][*] Membuka sesi Administrator via UAC... Silakan klik 'Yes' pada jendela konfirmasi.[/bold cyan]",
        title="[bold yellow]Auto-Elevation[/bold yellow]",
        border_style="yellow",
        padding=(1, 2)
    ))
    c.print("\n[bold cyan][*] Membuka jendela Administrator baru...[/bold cyan]")
    c.print("[dim]Prompt UAC Windows terpicu secara otomatis. Sesi non-administrator akan ditutup setelah elevasi disetujui.[/dim]")

# 2. Main Menu Screen
def draw_main_menu_screen(c: Console):
    draw_banner(c, is_admin=True)
    c.print("")
    c.print(f"[dim]Loaded {len(apps_data)} apps across 8 categories | Detected 14 installed packages.[/dim]\n")
    c.print("[bold]? What would you like to do?[/bold]")
    menus = [
        "Install Applications",
        "Persona Presets",
        "Filter by Category",
        "Search Winget Packages",
        "Upgrade Dashboard",
        "Debloat Windows (UWP)",
        "System & Explorer Tweaks",
        "Configure Terminal & PowerShell",
        "Setup Migration (Export / Import)",
        "Pre-Flight System Check",
        "Custom Profiles",
        "Refresh Installed Cache",
        "Add Custom Application",
        "Open apps.json in Editor",
        "Exit"
    ]
    for i, m in enumerate(menus):
        if i == 0:
            c.print(f" [bold cyan]❯ {m}[/bold cyan]")
        else:
            c.print(f"   {m}")

# 3. Checkbox Application Multi-Select Screen (Classic Dev ASCII [X]/[ ] style)
def draw_app_select_screen(c: Console):
    c.print("[bold cyan]=== Select Applications to Install ===[/bold cyan]")
    c.print("[dim](Space to select/deselect, 'a' to toggle all, 'i' to invert, Enter to confirm)[/dim]\n")
    c.print("[bold #89dceb]── WEB BROWSERS ──[/bold #89dceb]")
    c.print(" [bold #89dceb]❯[/bold #89dceb] [bold #6c7086][[/bold #6c7086][bold #a6e3a1]X[/bold #a6e3a1][bold #6c7086]][/bold #6c7086] [bold #cdd6f4]Mozilla Firefox[/bold #cdd6f4] [italic #89dceb][Installed][/italic #89dceb] [dim #6c7086](Mozilla.Firefox)[/dim #6c7086] [dim #a6adc8]- Fast, private, and open-source web browser[/dim #a6adc8]")
    c.print("   [bold #6c7086][[/bold #6c7086][bold #a6e3a1]X[/bold #a6e3a1][bold #6c7086]][/bold #6c7086] [bold #cdd6f4]Google Chrome[/bold #cdd6f4] [dim #6c7086](Google.Chrome)[/dim #6c7086] [dim #a6adc8]- Fast and secure web browser by Google[/dim #a6adc8]")
    c.print("   [bold #6c7086][ ][/bold #6c7086] [bold #cdd6f4]Brave Browser[/bold #cdd6f4] [dim #6c7086](Brave.Brave)[/dim #6c7086] [dim #a6adc8]- Privacy-focused browser with built-in ad blocker[/dim #a6adc8]")
    c.print("\n[bold #89dceb]── DEVELOPER TOOLS ──[/bold #89dceb]")
    c.print("   [bold #6c7086][[/bold #6c7086][bold #a6e3a1]X[/bold #a6e3a1][bold #6c7086]][/bold #6c7086] [bold #cdd6f4]Visual Studio Code[/bold #cdd6f4] [dim #6c7086](Microsoft.VisualStudioCode)[/dim #6c7086] [dim #a6adc8]- Code editing redefined by Microsoft[/dim #a6adc8]")
    c.print("   [bold #6c7086][[/bold #6c7086][bold #a6e3a1]X[/bold #a6e3a1][bold #6c7086]][/bold #6c7086] [bold #cdd6f4]Windows Terminal[/bold #cdd6f4] [dim #6c7086](Microsoft.WindowsTerminal)[/dim #6c7086] [dim #a6adc8]- Modern, fast, and powerful terminal for Windows[/dim #a6adc8]")
    c.print("   [bold #6c7086][[/bold #6c7086][bold #a6e3a1]X[/bold #a6e3a1][bold #6c7086]][/bold #6c7086] [bold #cdd6f4]PowerShell 7[/bold #cdd6f4] [dim #6c7086](Microsoft.PowerShell)[/dim #6c7086] [dim #a6adc8]- Cross-platform command-line shell[/dim #a6adc8]")
    c.print("   [bold #6c7086][[/bold #6c7086][bold #a6e3a1]X[/bold #a6e3a1][bold #6c7086]][/bold #6c7086] [bold #cdd6f4]Git[/bold #cdd6f4] [dim #6c7086](Git.Git)[/dim #6c7086] [dim #a6adc8]- Distributed version control system[/dim #a6adc8]")
    c.print("   [bold #6c7086][[/bold #6c7086][bold #a6e3a1]X[/bold #a6e3a1][bold #6c7086]][/bold #6c7086] [bold #cdd6f4]Node.js (LTS)[/bold #cdd6f4] [dim #6c7086](OpenJS.NodeJS.LTS)[/dim #6c7086] [dim #a6adc8]- JavaScript runtime built on Chrome's V8 engine[/dim #a6adc8]")
    c.print("\n[bold #89dceb]── MEDIA & AUDIO ──[/bold #89dceb]")
    c.print("   [bold #6c7086][[/bold #6c7086][bold #a6e3a1]X[/bold #a6e3a1][bold #6c7086]][/bold #6c7086] [bold #cdd6f4]VLC Media Player[/bold #cdd6f4] [dim #6c7086](VideoLAN.VLC)[/dim #6c7086] [dim #a6adc8]- Free and open source multimedia player[/dim #a6adc8]")
    c.print("   [bold #6c7086][[/bold #6c7086][bold #a6e3a1]X[/bold #a6e3a1][bold #6c7086]][/bold #6c7086] [bold #cdd6f4]Spotify[/bold #cdd6f4] [dim #6c7086](Spotify.Spotify)[/dim #6c7086] [dim #a6adc8]- Music for everyone[/dim #a6adc8]")
    c.print("   [bold #6c7086][ ][/bold #6c7086] [bold #cdd6f4]OBS Studio[/bold #cdd6f4] [dim #6c7086](OBSProject.OBSStudio)[/dim #6c7086] [dim #a6adc8]- Free and open source software for video recording[/dim #a6adc8]")

# 4. Persona Presets Screen
def draw_presets_screen(c: Console):
    c.print("[bold cyan]=== Persona Presets ===[/bold cyan]\n")
    table = Table(title="Available Preset Profiles", show_lines=True, border_style="cyan")
    table.add_column("Preset Name", style="bold green", width=26)
    table.add_column("Description", style="white", width=48)
    table.add_column("App Count", style="cyan", justify="center", width=12)
    
    for key, val in presets_data.items():
        table.add_row(f"{val.get('name', key)}", val.get("description", ""), f"{len(val.get('app_ids', []))} apps")
    c.print(table)
    c.print("\n[bold]? Choose a preset to inspect or install:[/bold]")
    c.print(" [bold cyan]❯ Developer Pack - Essential coding, terminal, shell, and developer tooling[/bold cyan]")
    c.print("   Gamer Pack - Gaming launchers, graphics tuning, controllers & voice chat")
    c.print("   Content Creator & Media - Streaming, recording, notes, audio enhancement & multimedia")
    c.print("   Minimalist & Essentials - Lightweight daily driver: browser, archive, PDF & local file sharing")
    c.print("   Power User & System Tuning - Advanced customization, deep clean, package management & terminal utilities")
    c.print("   Back")

# 5. Windows Debloater Screen
def draw_debloater_screen(c: Console):
    c.print("[bold red]=== Windows Bloatware Remover ===[/bold red]\n")
    table = Table(title="Pre-Configured Safe UWP Apps to Remove", show_lines=False, border_style="red")
    table.add_column("Status", justify="center", width=8)
    table.add_column("Package Name", style="bold white", width=32)
    table.add_column("Category / Target", style="dim", width=38)
    
    for item in debloat.DEBLOAT_LIST[:9]:
        table.add_row("[yellow]Detected[/yellow]", item["name"], item["description"])
    c.print(table)
    c.print("\n[bold]? Select Debloat Action:[/bold]")
    c.print(" [bold cyan]❯ Select bloatware packages to remove[/bold cyan]")
    c.print("   Quick debloat all recommended (Safe List)")
    c.print("   Back")

# 6. Windows Tweaks Screen
def draw_tweaks_screen(c: Console):
    c.print("[bold cyan]=== System & Explorer Tweaks ===[/bold cyan]\n")
    c.print("[dim]Each tweak includes automatic registry backup before modification with 1-click rollback.[/dim]\n")
    table = Table(title="Available Registry & Explorer Tweaks", show_lines=True, border_style="blue")
    table.add_column("Tweak Name", style="bold cyan", width=32)
    table.add_column("Description", style="white", width=52)
    table.add_column("Rollback Ready", justify="center", style="green", width=15)
    
    for tw in tweaks.TWEAKS_LIST:
        table.add_row(tw["name"], tw["description"], "[✓] Ready")
    c.print(table)
    c.print("\n[bold]? Choose Tweaks action:[/bold]")
    c.print(" [bold cyan]❯ Apply selected tweaks[/bold cyan]")
    c.print("   Revert tweaks to defaults")
    c.print("   Back")

# 7. Shell Booster Screen
def draw_shell_booster_screen(c: Console):
    c.print("[bold cyan]=== Terminal & PowerShell Profile ===[/bold cyan]\n")
    c.print(Panel(
        "[bold cyan]Powershell & Terminal Power Pack features:[/bold cyan]\n\n"
        " - [bold green]PSReadLine Predictive IntelliSense[/bold green]: History-based auto-suggestions.\n"
        " - [bold green]Starship Prompt[/bold green]: Blazing-fast, customizable cross-shell prompt.\n"
        " - [bold green]Power-User Aliases[/bold green]: 'll', 'grep', 'which', 'touch' for familiar terminal speed.\n"
        " - [bold green]UTF-8 Output Encoding[/bold green]: Clean Unicode and glyph rendering in console.",
        title="[bold green]Shell Booster Overview[/bold green]",
        border_style="green",
        padding=(1, 2)
    ))
    c.print("\n[bold]? What would you like to configure?[/bold]")
    c.print(" [bold cyan]❯ Apply modern PowerShell profile configuration[/bold cyan]")
    c.print("   Install and configure Starship Prompt")
    c.print("   Back")

# 8. Pre-Flight System Health Check Screen
def draw_preflight_screen(c: Console):
    c.print("[bold cyan]=== Pre-Flight System Check ===[/bold cyan]\n")
    table = Table(title="System Health Summary", show_lines=True, border_style="cyan")
    table.add_column("Diagnostic Item", style="bold white", width=25)
    table.add_column("Status", justify="center", width=15)
    table.add_column("Details", style="dim", width=45)
    
    table.add_row("Privilege Level", "[green]PASSED (Elevated)[/green]", "Sufficient privileges for registry & package installs")
    table.add_row("Winget Package Manager", "[green]PASSED (v1.9.x)[/green]", "Microsoft Winget is ready and responsive in PATH")
    table.add_row("Internet Connectivity", "[green]PASSED (Online)[/green]", "Connected to Winget CDN repository servers")
    table.add_row("System Drive Storage (C:)", "[green]PASSED (142.5 GB Free)[/green]", "Ample disk space available for batch installation")
    table.add_row("PowerShell Environment", "[green]PASSED (pwsh 7.4.x)[/green]", "Modern PowerShell 7 runtime detected")
    c.print(table)
    c.print("\n[bold green][✓] System is fully optimized and ready for installations![/bold green]")
    c.print("\n[dim]Press Enter to return to main menu...[/dim]")

# Render all SVG captures
render_to_svg("01_elevation_prompt.svg", draw_elevation_screen)
render_to_svg("02_main_menu.svg", draw_main_menu_screen)
render_to_svg("03_select_install_apps.svg", draw_app_select_screen)
render_to_svg("04_persona_presets.svg", draw_presets_screen)
render_to_svg("05_debloater.svg", draw_debloater_screen)
render_to_svg("06_system_tweaks.svg", draw_tweaks_screen)
render_to_svg("07_shell_booster.svg", draw_shell_booster_screen)
render_to_svg("08_preflight_health.svg", draw_preflight_screen)

print("All feature SVGs rendered successfully!")
