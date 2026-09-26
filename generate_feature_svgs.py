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
from PIL import Image, ImageDraw, ImageFont

# Import internal modules
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

# 1. Main Banner & Elevation Screen
def draw_elevation_screen(c: Console):
    title = """
  ██╗    ██╗██╗███╗   ██╗      ███████╗██████╗ ███████╗███████╗██╗  ██╗
  ██║    ██║██║████╗  ██║      ██╔════╝██╔══██╗██╔════╝██╔════╝██║  ██║
  ██║ █╗ ██║██║██╔██╗ ██║█████╗█████╗  ██████╔╝█████╗  ███████╗███████║
  ██║███╗██║██║██║╚██╗██║╚════╝██╔══╝  ██╔══██╗██╔══╝  ╚════██║██╔══██║
  ╚███╔███╔╝██║██║ ╚████║      ██║     ██║  ██║███████╗███████║██║  ██║
   ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝      ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
    """
    c.print(Align.center(f"[bold cyan]{title}[/bold cyan]"))
    c.print(Align.center("[bold white]Windows 11 & 10 Automated Package & System Setup Suite[/bold white]"))
    c.print(Align.center("[dim]Author: Hilal06 | GitHub: https://github.com/Hilal06/win-fresh-setup[/dim]\n"))
    c.print(Panel(
        "[bold yellow]⚠️  PEMBERITAHUAN HAK AKSES SISTEM[/bold yellow]\n\n"
        "Anda saat ini menjalankan installer sebagai [bold cyan]Standard User (Bukan Administrator)[/bold cyan].\n\n"
        "Fitur seperti [italic]Instalasi Aplikasi System-wide, Registry Tweaks, Windows Debloater, dan Shell Booster[/italic] "
        "memerlukan hak akses [bold green]Administrator[/bold green] agar dapat bekerja secara optimal.\n\n"
        "[bold green]👉 Catatan: Sangat direkomendasikan untuk beralih ke sesi Administrator sekarang.[/bold green]",
        title="[bold yellow]🛡️ Hak Akses Administrator[/bold yellow]",
        border_style="yellow",
        padding=(1, 2)
    ))
    c.print("\n[bold]? Pilih mode eksekusi:[/bold]")
    c.print("  [bold green]❯ 🛡️ Beralih ke Administrator (Sangat Direkomendasikan)[/bold green]")
    c.print("    👤 Tetap Lanjut sebagai Standard User (Beberapa fitur mungkin terbatas)")
    c.print("    ❌ Keluar")

# 2. Main Menu Screen
def draw_main_menu_screen(c: Console):
    title = """
  ██╗    ██╗██╗███╗   ██╗      ███████╗██████╗ ███████╗███████╗██╗  ██╗
  ██║    ██║██║████╗  ██║      ██╔════╝██╔══██╗██╔════╝██╔════╝██║  ██║
  ██║ █╗ ██║██║██╔██╗ ██║█████╗█████╗  ██████╔╝█████╗  ███████╗███████║
  ██║███╗██║██║██║╚██╗██║╚════╝██╔══╝  ██╔══██╗██╔══╝  ╚════██║██╔══██║
  ╚███╔███╔╝██║██║ ╚████║      ██║     ██║  ██║███████╗███████║██║  ██║
   ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝      ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
    """
    c.print(Align.center(f"[bold cyan]{title}[/bold cyan]"))
    c.print(Align.center("[bold white]Windows 11 & 10 Automated Package & System Setup Suite[/bold white]"))
    c.print(Align.center("[dim]Author: Hilal06 | GitHub: https://github.com/Hilal06/win-fresh-setup[/dim]\n"))
    c.print(f"[dim]Loaded {len(apps_data)} apps across 7 categories | Detected 14 installed packages.[/dim]\n")
    c.print("[bold]? What would you like to do?[/bold]")
    menus = [
        "🚀 Select & Install Apps (Full Checkbox TUI)",
        "🎯 Curated Persona Presets (Dev, Gamer, Creator, Minimalist...)",
        "📂 Filter & Select by Category",
        "🔍 Live In-App Winget Search (Find & Install on the fly)",
        "📊 Interactive Updates Dashboard (Installed vs Latest)",
        "🧹 Windows Bloatware Remover (Debloater)",
        "🛠️ Windows System & Explorer Tweaks (with Rollback)",
        "⚡ Boost PowerShell & Terminal (Starship, Aliases & IntelliSense)",
        "💾 PC Setup Migration (Backup & Restore Software Inventory)",
        "🩺 System Pre-Flight & Health Check",
        "💾 Custom Profiles (Save / Load Custom App Bundles)",
        "➕ Add New App to apps.json",
        "📝 Open apps.json in Default Text Editor",
        "❌ Exit"
    ]
    for i, m in enumerate(menus):
        if i == 0:
            c.print(f" [bold magenta]❯ {m}[/bold magenta]")
        else:
            c.print(f"   {m}")

# 3. Checkbox Application Multi-Select Screen
def draw_app_select_screen(c: Console):
    c.print("[bold yellow]=== 🚀 Select & Install Applications ===[/bold yellow]")
    c.print("[dim](Space to select/deselect, 'a' to toggle all, 'i' to invert, Enter to confirm)[/dim]\n")
    c.print("[bold cyan]-- Web Browsers --[/bold cyan]")
    c.print(" [bold green]❯ [X] Mozilla Firefox - Fast, private, and open-source web browser (Mozilla.Firefox)[/bold green]")
    c.print("   [X] Google Chrome - Fast and secure web browser by Google (Google.Chrome)")
    c.print("   [ ] Brave Browser - Privacy-focused browser with built-in ad blocker (Brave.Brave)")
    c.print("\n[bold cyan]-- Developer Tools --[/bold cyan]")
    c.print("   [X] Visual Studio Code - Code editing redefined by Microsoft (Microsoft.VisualStudioCode)")
    c.print("   [X] Windows Terminal - Modern, fast, and powerful terminal for Windows (Microsoft.WindowsTerminal)")
    c.print("   [X] PowerShell 7 - Cross-platform command-line shell (Microsoft.PowerShell)")
    c.print("   [X] Git - Distributed version control system (Git.Git)")
    c.print("   [X] Node.js (LTS) - JavaScript runtime built on Chrome's V8 engine (OpenJS.NodeJS.LTS)")
    c.print("\n[bold cyan]-- Media & Audio --[/bold cyan]")
    c.print("   [X] VLC Media Player - Free and open source multimedia player (VideoLAN.VLC)")
    c.print("   [X] Spotify - Music for everyone (Spotify.Spotify)")
    c.print("   [ ] OBS Studio - Free and open source software for video recording (OBSProject.OBSStudio)")

# 4. Persona Presets Screen
def draw_presets_screen(c: Console):
    c.print("[bold yellow]=== 🎯 Curated Persona Presets ===[/bold yellow]\n")
    table = Table(title="Available Preset Profiles", show_lines=True, border_style="cyan")
    table.add_column("Preset Name", style="bold green", width=26)
    table.add_column("Description", style="white", width=48)
    table.add_column("App Count", style="cyan", justify="center", width=12)
    
    for key, val in presets_data.items():
        table.add_row(f"{val.get('name', key)}", val.get("description", ""), f"{len(val.get('app_ids', []))} apps")
    c.print(table)
    c.print("\n[bold]? Choose a preset to inspect or install:[/bold]")
    c.print(" [bold magenta]❯ 💻 Developer Pack - Essential coding, terminal, shell, and developer tooling[/bold magenta]")
    c.print("   🎮 Gamer Pack - Gaming launchers, graphics tuning, controllers & voice chat")
    c.print("   🎬 Content Creator & Media - Streaming, recording, notes, audio enhancement & multimedia")
    c.print("   🪶 Minimalist Pack - Lightweight daily essentials without clutter")
    c.print("   ⚡ Power User Pack - Complete system utilities, tweaks, uninstallers & monitors")

# 5. Windows Debloater Screen
def draw_debloater_screen(c: Console):
    c.print("[bold yellow]=== 🧹 Windows Bloatware Remover (Debloater) ===[/bold yellow]\n")
    table = Table(title="Pre-Configured Safe UWP Apps to Remove", show_lines=False, border_style="red")
    table.add_column("Status", justify="center", width=8)
    table.add_column("Package Name", style="bold white", width=32)
    table.add_column("Category / Target", style="dim", width=38)
    
    for item in debloat.DEBLOAT_LIST[:9]:
        table.add_row("[yellow]Detected[/yellow]", item["name"], item["description"])
    c.print(table)
    c.print("\n[bold]? Select Debloat Action:[/bold]")
    c.print(" [bold magenta]❯ 🎯 Selective Debloat (Choose which apps to uninstall)[/bold magenta]")
    c.print("   ⚡ Quick Debloat All Recommended (Safe List)")
    c.print("   ← Back to Main Menu")

# 6. Windows Tweaks Screen
def draw_tweaks_screen(c: Console):
    c.print("[bold yellow]=== 🛠️ Windows System & Explorer Tweaks ===[/bold yellow]\n")
    c.print("[dim]Each tweak includes automatic registry backup before modification with 1-click rollback.[/dim]\n")
    table = Table(title="Available Registry & Explorer Tweaks", show_lines=True, border_style="blue")
    table.add_column("Tweak Name", style="bold cyan", width=28)
    table.add_column("Description", style="white", width=55)
    table.add_column("Rollback Ready", justify="center", style="green", width=15)
    
    for tw in tweaks.TWEAKS_LIST:
        table.add_row(tw["name"], tw["description"], "✓ Yes")
    c.print(table)
    c.print("\n[bold]? Choose Tweaks action:[/bold]")
    c.print(" [bold magenta]❯ 🚀 Apply Tweaks (Select from list)[/bold magenta]")
    c.print("   🔄 Revert / Rollback Tweaks to Default")
    c.print("   ← Back to Main Menu")

# 7. Shell Booster Screen
def draw_shell_booster_screen(c: Console):
    c.print("[bold yellow]=== ⚡ Boost PowerShell & Terminal ===[/bold yellow]\n")
    c.print(Panel(
        "[bold cyan]Powershell & Terminal Power Pack features:[/bold cyan]\n\n"
        " • [bold green]PSReadLine Predictive IntelliSense[/bold green]: Fish-shell style auto-completion & history search.\n"
        " • [bold green]Starship Prompt[/bold green]: Blazing-fast, customizable, cross-shell prompt.\n"
        " • [bold green]Power-User Aliases[/bold green]: 'll', 'grep', 'which', 'touch' for familiar Unix terminal speed.\n"
        " • [bold green]Windows Terminal Profiles[/bold green]: Clean UTF-8 font and prompt rendering.",
        title="[bold green]Shell Booster Overview[/bold green]",
        border_style="green",
        padding=(1, 2)
    ))
    c.print("\n[bold]? What would you like to configure?[/bold]")
    c.print(" [bold magenta]❯ 🚀 Auto-Configure All (IntelliSense + Starship + Aliases)[/bold magenta]")
    c.print("   🛠️ Configure PSReadLine Predictive IntelliSense only")
    c.print("   ⭐ Install and Setup Starship Cross-Shell Prompt")
    c.print("   ← Back to Main Menu")

# 8. Pre-Flight System Health Check Screen
def draw_preflight_screen(c: Console):
    c.print("[bold yellow]=== 🩺 System Pre-Flight & Health Check ===[/bold yellow]\n")
    table = Table(title="Windows Environment Pre-Flight Diagnosis", show_lines=True, border_style="cyan")
    table.add_column("Diagnostic Item", style="bold white", width=25)
    table.add_column("Status", justify="center", width=15)
    table.add_column("Details", style="dim", width=45)
    
    table.add_row("Administrator Rights", "[green]PASSED (Elevated)[/green]", "Sufficient privileges for registry & package installs")
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
