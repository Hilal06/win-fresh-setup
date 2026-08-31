#!/usr/bin/env python3
"""
win-fresh-setup - Windows 11 & 10 Automated Package & System Setup Suite
Author: Hilal06
Repository: https://github.com/Hilal06/win-fresh-setup

Features:
- Interactive TUI multi-select with search and categories (via questionary & rich)
- Curated Persona Presets (Developer, Gamer, Creator, Minimalist, Power User)
- Windows System & Explorer Tweaks with automatic Registry Backup & Rollback
- Live In-App Winget Search ("Search & Install on the fly")
- Windows Bloatware Remover & Debloater (UWP AppxPackage removal)
- PC Setup Migration & Backup (Export / Import installed software inventory)
- Interactive Upgrade Dashboard (View Outdated vs Latest version)
- PowerShell & Terminal Booster (PSReadLine Predictive IntelliSense, Starship, Aliases)
- Pre-Flight System Health & Disk Space Check
- Pre-scan already installed applications to prevent redundant installations
- Administrator privileges detection
- Custom profile Save & Load system
- Persistent installation logging
"""

import sys
import os
import json
import subprocess
import shutil
import ctypes
import socket
import urllib.request
from datetime import datetime
from typing import List, Dict, Any, Optional, Set, Tuple

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    import questionary
    from questionary import Choice, Separator, Style
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.align import Align
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich import print as rprint
except ImportError:
    print("[!] Missing required packages. Please install requirements:")
    print("    pip install -r requirements.txt")
    sys.exit(1)

import tweaks
import debloat
import shell_booster

CONSOLE = Console()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APPS_FILE = os.path.join(BASE_DIR, "apps.json")
PRESETS_FILE = os.path.join(BASE_DIR, "presets.json")
PROFILES_FILE = os.path.join(BASE_DIR, "custom_profiles.json")
TITLE_FILE = os.path.join(BASE_DIR, "title.txt")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

_INSTALLED_CACHE: Optional[Set[str]] = None

# Custom styling for questionary
CUSTOM_STYLE = Style([
    ('qmark', 'fg:#5f87ff bold'),
    ('question', 'bold'),
    ('answer', 'fg:#5fffff bold'),
    ('pointer', 'fg:#ff5f87 bold'),
    ('highlighted', 'fg:#ff5f87 bold'),
    ('selected', 'fg:#5fff87 bold'),
    ('separator', 'fg:#6c6c6c italic'),
    ('instruction', 'fg:#808080 italic'),
    ('text', ''),
    ('disabled', 'fg:#858585 italic')
])

def is_admin() -> bool:
    """Check if the script is running with elevated Administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def ensure_dirs():
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR, exist_ok=True)

def load_title() -> str:
    """Load ASCII art title from title.txt with a safe fallback."""
    if os.path.exists(TITLE_FILE):
        try:
            with open(TITLE_FILE, "r", encoding="utf-8") as f:
                content = f.read().rstrip()
                if content:
                    return content
        except Exception:
            pass
    return (
        "██╗░░██╗██╗██╗░░░░░░█████╗░██╗░░░░░░█████╗░░█████╗░\n"
        "██║░░██║██║██║░░░░░██╔══██╗██║░░░░░██╔══██╗██╔═══╝░\n"
        "███████║██║██║░░░░░███████║██║░░░░░██║░░██║██████╗░\n"
        "██╔══██║██║██║░░░░░██╔══██║██║░░░░░██║░░██║██╔══██╗\n"
        "██║░░██║██║███████╗██║░░██║███████╗╚█████╔╝╚█████╔╝\n"
        "╚═╝░░╚═╝╚═╝╚══════╝╚═╝░░╚═╝╚══════╝░╚════╝░░╚════╝░"
    )

def print_banner():
    CONSOLE.clear()
    admin_status = "[bold green][🛡️ Administrator][/bold green]" if is_admin() else "[dim yellow][👤 Standard User][/dim yellow]"
    title_art = load_title()
    banner_content = (
        f"[bold #ff8800]{title_art}[/bold #ff8800]\n\n"
        f"[bold cyan]win-fresh-setup[/bold cyan]  {admin_status}\n"
        f"[dim]Windows 11 & 10 Automated Package & System Setup TUI[/dim]\n"
        f"[italic magenta]Developed by Hilal06[/italic magenta]"
    )
    CONSOLE.print(Align.center(Panel(Align.center(banner_content), border_style="orange3", expand=False)))

def check_winget() -> bool:
    """Check if winget CLI is accessible."""
    return shutil.which("winget") is not None

def parse_winget_table(output: str) -> List[Dict[str, str]]:
    """Parse fixed-width tabular output from winget search/upgrade/list."""
    lines = output.splitlines()
    dash_idx = -1
    for idx, line in enumerate(lines):
        if line.strip() and set(line.strip().replace(" ", "")) == {"-"}:
            dash_idx = idx
            break
    if dash_idx <= 0:
        return []

    header = lines[dash_idx - 1]
    name_pos = header.find("Name")
    id_pos = header.find("Id")
    ver_pos = header.find("Version")
    avail_pos = header.find("Available")
    if avail_pos == -1:
        avail_pos = header.find("Match")
    src_pos = header.find("Source")

    results = []
    for line in lines[dash_idx + 1:]:
        line_str = line.strip()
        if not line_str or "upgrades available" in line_str.lower() or "have been found" in line_str.lower():
            continue
        if len(line) < id_pos:
            continue

        name = line[name_pos:id_pos].strip() if id_pos != -1 else ""
        id_val = line[id_pos:ver_pos].strip() if ver_pos != -1 else line[id_pos:].strip()

        if ver_pos != -1:
            next_pos = avail_pos if avail_pos != -1 else src_pos
            ver_val = line[ver_pos:next_pos].strip() if next_pos != -1 else line[ver_pos:].strip()
        else:
            ver_val = ""

        if avail_pos != -1:
            avail_val = line[avail_pos:src_pos].strip() if src_pos != -1 else line[avail_pos:].strip()
        else:
            avail_val = ""

        src_val = line[src_pos:].strip() if src_pos != -1 else "winget"

        if id_val:
            results.append({
                "name": name,
                "id": id_val,
                "version": ver_val,
                "available": avail_val,
                "source": src_val
            })
    return results

def scan_installed_apps(force_refresh: bool = False) -> Set[str]:
    """Scan machine using winget list to detect already installed packages."""
    global _INSTALLED_CACHE
    if _INSTALLED_CACHE is not None and not force_refresh:
        return _INSTALLED_CACHE

    installed = set()
    try:
        res = subprocess.run(
            ["winget", "list", "--accept-source-agreements"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=25
        )
        if res.returncode == 0:
            for item in parse_winget_table(res.stdout):
                installed.add(item["id"].lower())
                installed.add(item["name"].lower())
    except Exception as e:
        CONSOLE.print(f"[dim yellow][!] Note: Quick installed scan skipped ({e})[/dim yellow]")

    _INSTALLED_CACHE = installed
    return installed

def load_apps() -> List[Dict[str, Any]]:
    """Load application list from apps.json."""
    if not os.path.exists(APPS_FILE):
        CONSOLE.print(f"[bold red][!] Config file not found:[/bold red] {APPS_FILE}")
        return []
    try:
        with open(APPS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        CONSOLE.print(f"[bold red][!] Error parsing {APPS_FILE}:[/bold red] {e}")
        return []

def save_apps(apps: List[Dict[str, Any]]) -> bool:
    """Save application list back to apps.json."""
    try:
        with open(APPS_FILE, "w", encoding="utf-8") as f:
            json.dump(apps, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        CONSOLE.print(f"[bold red][!] Error saving apps.json:[/bold red] {e}")
        return False

def load_presets() -> Dict[str, Any]:
    """Load preset bundles from presets.json."""
    if not os.path.exists(PRESETS_FILE):
        return {}
    try:
        with open(PRESETS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def load_custom_profiles() -> Dict[str, Any]:
    """Load custom saved profiles."""
    if not os.path.exists(PROFILES_FILE):
        return {}
    try:
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_custom_profiles(profiles: Dict[str, Any]) -> bool:
    """Save custom profiles."""
    try:
        with open(PROFILES_FILE, "w", encoding="utf-8") as f:
            json.dump(profiles, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def is_app_installed(app: Dict[str, Any], installed_set: Set[str]) -> bool:
    """Check if app ID is found in installed set."""
    app_id = app.get("id", "").lower()
    return app_id in installed_set

def build_choices(
    apps: List[Dict[str, Any]],
    filter_cat: Optional[str] = None,
    target_ids: Optional[Set[str]] = None,
    installed_set: Optional[Set[str]] = None
) -> List[Any]:
    """Construct Questionary choice list grouped with category separators and installed badges."""
    if installed_set is None:
        installed_set = set()

    categorized: Dict[str, List[Dict[str, Any]]] = {}
    for app in apps:
        cat = app.get("category", "General")
        if filter_cat and cat != filter_cat:
            continue
        categorized.setdefault(cat, []).append(app)

    choices = []
    for cat_name in sorted(categorized.keys()):
        choices.append(Separator(f"── {cat_name.upper()} ──"))
        for app in categorized[cat_name]:
            app_id = app.get("id", "")
            installed = is_app_installed(app, installed_set)

            badge = " [Installed]" if installed else ""
            display_title = f"{app['name']}{badge} [dim]({app_id})[/dim]"
            if app.get("description"):
                display_title += f" - {app['description']}"

            # Checked state logic:
            if target_ids is not None:
                is_checked = app_id in target_ids
            else:
                is_checked = False if installed else app.get("default", False)

            choices.append(Choice(
                title=display_title,
                value=app,
                checked=is_checked
            ))
    return choices

def run_winget_install(app: Dict[str, Any], log_file_path: str) -> Dict[str, Any]:
    """Execute winget install command for a specific application."""
    app_id = app["id"]
    name = app["name"]

    cmd = [
        "winget", "install",
        "--id", app_id,
        "-e",
        "--accept-package-agreements",
        "--accept-source-agreements",
        "--disable-interactivity"
    ]

    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"\n{'='*50}\n")
        log_file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Installing {name} ({app_id})\n")
        log_file.write(f"Command: {' '.join(cmd)}\n")
        log_file.write(f"{'='*50}\n")

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace"
            )

            output_lines = []
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    log_file.write(line)
                    log_file.flush()
                    output_lines.append(line.strip())

            returncode = process.poll()
            output_text = "\n".join(output_lines)

            if returncode == 0:
                if "Successfully installed" in output_text or "Installation completed" in output_text:
                    return {"status": "SUCCESS", "message": "Installed successfully"}
                else:
                    return {"status": "SUCCESS", "message": "Completed"}
            elif returncode in [-1978335189, 2316632107] or "already installed" in output_text.lower():
                return {"status": "ALREADY_INSTALLED", "message": "Already installed"}
            elif "No package found" in output_text:
                return {"status": "NOT_FOUND", "message": "Package ID not found in Winget"}
            else:
                last_err = output_lines[-2:] if len(output_lines) >= 2 else output_lines
                err_msg = " | ".join(last_err) if last_err else f"Exit code {returncode}"
                return {"status": "FAILED", "message": err_msg[:60]}

        except Exception as e:
            log_file.write(f"Exception during execution: {str(e)}\n")
            return {"status": "FAILED", "message": str(e)}

def execute_installation(selected_apps: List[Dict[str, Any]]):
    """Run sequential installation of selected packages with live rich progress and retry queue."""
    if not selected_apps:
        CONSOLE.print("[bold yellow]No applications selected.[/bold yellow]")
        questionary.press_any_key_to_continue().ask()
        return

    ensure_dirs()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_path = os.path.join(LOGS_DIR, f"winget_install_{timestamp}.log")

    print_banner()
    table = Table(title=f"Ready to Install ({len(selected_apps)} Apps)", show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Category", style="cyan", width=22)
    table.add_column("App Name", style="bold white", width=25)
    table.add_column("Winget ID", style="green", width=30)

    for idx, app in enumerate(selected_apps, 1):
        table.add_row(str(idx), app.get("category", "General"), app["name"], app["id"])

    CONSOLE.print(table)
    CONSOLE.print(f"[dim]Log file will be saved to: {log_file_path}[/dim]\n")

    confirm = questionary.confirm("Start installation now?", default=True).ask()
    if not confirm:
        return

    results = []
    CONSOLE.print("\n[bold cyan]Starting Winget Installation Queue...[/bold cyan]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=CONSOLE
    ) as progress:
        overall_task = progress.add_task("[cyan]Overall Progress[/cyan]", total=len(selected_apps))

        for idx, app in enumerate(selected_apps, 1):
            progress.update(overall_task, description=f"[cyan]Installing ({idx}/{len(selected_apps)}):[/cyan] [bold white]{app['name']}[/bold white]")

            res = run_winget_install(app, log_file_path)
            res["app"] = app
            results.append(res)

            if res["status"] == "SUCCESS":
                CONSOLE.print(f"  [bold green][✓] {app['name']}[/bold green] - Installed successfully")
            elif res["status"] == "ALREADY_INSTALLED":
                CONSOLE.print(f"  [bold yellow][i] {app['name']}[/bold yellow] - Already installed")
            elif res["status"] == "NOT_FOUND":
                CONSOLE.print(f"  [bold red][✗] {app['name']}[/bold red] - Package ID not found ({app['id']})")
            else:
                CONSOLE.print(f"  [bold red][✗] {app['name']}[/bold red] - Failed: {res['message']}")

            progress.advance(overall_task)

    CONSOLE.print("\n")
    summary_table = Table(title="Installation Summary Report", show_header=True, header_style="bold cyan")
    summary_table.add_column("App Name", style="bold white", width=25)
    summary_table.add_column("Winget ID", style="dim", width=28)
    summary_table.add_column("Status", width=18)
    summary_table.add_column("Details", width=35)

    success_cnt = 0
    already_cnt = 0
    failed_apps = []

    for r in results:
        app = r["app"]
        status = r["status"]
        if status == "SUCCESS":
            status_str = "[green]✓ Installed[/green]"
            success_cnt += 1
        elif status == "ALREADY_INSTALLED":
            status_str = "[yellow]ℹ Already Present[/yellow]"
            already_cnt += 1
        else:
            status_str = "[red]✗ Failed[/red]"
            failed_apps.append(app)

        summary_table.add_row(app["name"], app["id"], status_str, r["message"])

    CONSOLE.print(summary_table)
    CONSOLE.print(
        f"\n[bold]Results:[/bold] "
        f"[green]{success_cnt} Installed[/green] | "
        f"[yellow]{already_cnt} Already Present[/yellow] | "
        f"[red]{len(failed_apps)} Failed[/red]"
    )
    CONSOLE.print(f"[dim]Full logs saved to: {log_file_path}[/dim]\n")

    # Retry Queue for Failed Installations
    if failed_apps:
        retry = questionary.confirm(f"⚠️ {len(failed_apps)} app(s) failed. Would you like to retry them now?", default=True).ask()
        if retry:
            execute_installation(failed_apps)
            return

    scan_installed_apps(force_refresh=True)
    questionary.press_any_key_to_continue().ask()

def handle_winget_search_menu(apps: List[Dict[str, Any]]):
    """Live In-App Winget Search with instant install and bookmarking."""
    print_banner()
    CONSOLE.print("[bold cyan]=== 🔍 Live In-App Winget Search ===[/bold cyan]\n")

    query = questionary.text("Enter search keyword (e.g. vlc, obsidian, blender, figma):").ask()
    if not query or not query.strip():
        return

    CONSOLE.print(f"\n[dim]Searching Winget repositories for '{query}'...[/dim]")
    try:
        res = subprocess.run(
            ["winget", "search", query.strip(), "--accept-source-agreements"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30
        )
        results = parse_winget_table(res.stdout)
    except Exception as e:
        CONSOLE.print(f"[bold red]Search failed: {e}[/bold red]")
        questionary.press_any_key_to_continue().ask()
        return

    if not results:
        CONSOLE.print(f"[yellow]No packages matching '{query}' found.[/yellow]")
        questionary.press_any_key_to_continue().ask()
        return

    table = Table(title=f"Search Results for '{query}' ({len(results)} found)", show_header=True, header_style="bold cyan")
    table.add_column("#", style="dim", width=4)
    table.add_column("Name", style="bold white", width=28)
    table.add_column("Package ID", style="green", width=32)
    table.add_column("Version", style="dim", width=14)
    table.add_column("Source", style="cyan", width=10)

    for idx, r in enumerate(results[:15], 1):
        table.add_row(str(idx), r["name"][:27], r["id"][:31], r["version"][:13], r["source"][:9])

    CONSOLE.print(table)

    item_choices = [
        Choice(f"{r['name']} ({r['id']})", value=r)
        for r in results[:15]
    ] + [Choice("← Cancel / Back", value=None)]

    chosen_pkg = questionary.select("Select a package to take action:", choices=item_choices, style=CUSTOM_STYLE).ask()
    if not chosen_pkg:
        return

    action = questionary.select(
        f"Action for [{chosen_pkg['name']}]:",
        choices=[
            Choice("⚡ Install Immediately", value="install"),
            Choice("➕ Add to apps.json permanently", value="add_json"),
            Choice("⚡ Install AND Add to apps.json", value="both"),
            Choice("← Cancel", value="cancel")
        ],
        style=CUSTOM_STYLE
    ).ask()

    app_entry = {
        "category": "Custom & Tools",
        "name": chosen_pkg["name"],
        "id": chosen_pkg["id"],
        "description": f"Version {chosen_pkg['version']} from {chosen_pkg['source']}",
        "default": True
    }

    if action in ["add_json", "both"]:
        apps.append(app_entry)
        save_apps(apps)
        CONSOLE.print(f"[bold green][✓] Added '{chosen_pkg['name']}' ({chosen_pkg['id']}) to apps.json![/bold green]")

    if action in ["install", "both"]:
        execute_installation([app_entry])
    elif action == "add_json":
        questionary.press_any_key_to_continue().ask()

def handle_debloat_menu():
    """Handle Windows Bloatware Remover."""
    print_banner()
    CONSOLE.print("[bold red]=== 🧹 Windows Bloatware Remover (Debloater) ===[/bold red]\n")
    CONSOLE.print("[dim]Select pre-installed Windows UWP apps you wish to safely uninstall:[/dim]\n")

    choices = []
    for item in debloat.DEBLOAT_LIST:
        display_title = f"{item['name']} - [dim]{item['description']}[/dim]"
        choices.append(Choice(
            title=display_title,
            value=item["id"],
            checked=item.get("default", False)
        ))

    selected_ids = questionary.checkbox(
        "Select bloatware apps to uninstall:",
        choices=choices,
        instruction="(Space: toggle, 'a': select all, Enter: remove, Ctrl+C: back)",
        style=CUSTOM_STYLE
    ).ask()

    if not selected_ids:
        return

    confirm = questionary.confirm(f"⚠️ Are you sure you want to uninstall {len(selected_ids)} selected bloatware package(s)?", default=True).ask()
    if not confirm:
        return

    CONSOLE.print("\n[bold cyan]Removing Selected Bloatware Packages...[/bold cyan]\n")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=CONSOLE
    ) as progress:
        task = progress.add_task("[cyan]Debloating...[/cyan]", total=len(selected_ids))
        results = []
        for pkg_id in selected_ids:
            progress.update(task, description=f"[cyan]Uninstalling:[/cyan] [bold white]{pkg_id}[/bold white]")
            success = debloat.uninstall_appx_package(pkg_id)
            pkg_info = next((x for x in debloat.DEBLOAT_LIST if x["id"] == pkg_id), {"name": pkg_id, "description": ""})
            results.append({"name": pkg_info["name"], "id": pkg_id, "success": success})
            progress.advance(task)

    CONSOLE.print("\n")
    table = Table(title="Debloat Summary Report", show_header=True, header_style="bold cyan")
    table.add_column("App Name", style="bold white", width=32)
    table.add_column("Package Pattern", style="dim", width=35)
    table.add_column("Status", width=15)

    for r in results:
        status_str = "[green]✓ Removed[/green]" if r["success"] else "[yellow]ℹ Not Installed / Skipped[/yellow]"
        table.add_row(r["name"], r["id"], status_str)

    CONSOLE.print(table)
    CONSOLE.print("[bold green][✓] Debloat operation completed![/bold green]")
    questionary.press_any_key_to_continue().ask()

def handle_migration_menu(apps: List[Dict[str, Any]], installed_set: Set[str]):
    """Handle PC Setup Migration (Backup & Restore)."""
    print_banner()
    CONSOLE.print("[bold cyan]=== 💾 PC Setup Migration (Backup & Restore) ===[/bold cyan]\n")

    choices = [
        Choice("📤 Export Current PC Software Inventory to JSON", value="export"),
        Choice("📥 Import & Batch-Install from Backup JSON", value="import"),
        Choice("← Back", value="back")
    ]

    action = questionary.select("Select Migration Action:", choices=choices, style=CUSTOM_STYLE).ask()
    if action == "back" or action is None:
        return

    if action == "export":
        ensure_dirs()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_file = os.path.join(BASE_DIR, f"my-system-setup-{timestamp}.json")
        out_path = questionary.text(f"Save setup inventory file to:", default=default_file).ask()
        if not out_path:
            return

        CONSOLE.print("\n[dim]Scanning all installed Winget applications on this PC...[/dim]")
        try:
            res = subprocess.run(
                ["winget", "list", "--accept-source-agreements"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30
            )
            detected_items = parse_winget_table(res.stdout)
            export_payload = {
                "created_at": datetime.now().isoformat(),
                "hostname": socket.gethostname(),
                "apps": [
                    {
                        "name": item["name"],
                        "id": item["id"],
                        "version": item["version"],
                        "source": item["source"]
                    }
                    for item in detected_items if item["source"].lower() == "winget"
                ]
            }

            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(export_payload, f, indent=2, ensure_ascii=False)

            CONSOLE.print(f"[bold green][✓] Exported {len(export_payload['apps'])} installed apps successfully to:[/bold green]\n{out_path}")
        except Exception as e:
            CONSOLE.print(f"[bold red]Export failed: {e}[/bold red]")

        questionary.press_any_key_to_continue().ask()

    elif action == "import":
        file_path = questionary.text("Enter path to backup JSON file to import:").ask()
        if not file_path or not os.path.exists(file_path):
            CONSOLE.print("[bold red]File not found.[/bold red]")
            questionary.press_any_key_to_continue().ask()
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            imported_apps = data.get("apps", data if isinstance(data, list) else [])
            converted_apps = [
                {
                    "category": "Imported Backup",
                    "name": a.get("name", a.get("id")),
                    "id": a.get("id"),
                    "description": f"Version {a.get('version', 'latest')}",
                    "default": True
                }
                for a in imported_apps if a.get("id")
            ]

            if not converted_apps:
                CONSOLE.print("[yellow]No valid applications found in backup file.[/yellow]")
                questionary.press_any_key_to_continue().ask()
                return

            choices = build_choices(converted_apps, installed_set=installed_set)
            selected = questionary.checkbox(
                f"Select imported apps to install ({len(converted_apps)} found):",
                choices=choices,
                style=CUSTOM_STYLE
            ).ask()

            if selected:
                execute_installation(selected)
        except Exception as e:
            CONSOLE.print(f"[bold red]Import failed: {e}[/bold red]")
            questionary.press_any_key_to_continue().ask()

def handle_upgrade_dashboard():
    """Interactive dashboard for checking and upgrading outdated applications."""
    print_banner()
    CONSOLE.print("[bold cyan]=== 📊 Interactive Upgrade Dashboard ===[/bold cyan]\n")
    CONSOLE.print("[dim]Checking Winget for available software updates...[/dim]\n")

    try:
        res = subprocess.run(
            ["winget", "upgrade", "--include-unknown", "--accept-source-agreements"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=35
        )
        upgrades = parse_winget_table(res.stdout)
    except Exception as e:
        CONSOLE.print(f"[bold red]Failed to check upgrades: {e}[/bold red]")
        questionary.press_any_key_to_continue().ask()
        return

    if not upgrades:
        CONSOLE.print("[bold green][✓] All installed applications are currently up to date![/bold green]")
        questionary.press_any_key_to_continue().ask()
        return

    table = Table(title=f"Outdated Applications ({len(upgrades)} Updates Available)", show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Application Name", style="bold white", width=28)
    table.add_column("Package ID", style="green", width=30)
    table.add_column("Installed", style="yellow", width=14)
    table.add_column("Latest", style="bold green", width=14)

    for idx, u in enumerate(upgrades, 1):
        table.add_row(str(idx), u["name"][:27], u["id"][:29], u["version"][:13], u["available"][:13])

    CONSOLE.print(table)

    choices = [
        Choice("🚀 Upgrade All Outdated Apps", value="all"),
        Choice("🎯 Select Specific Apps to Upgrade", value="select"),
        Choice("← Back", value="back")
    ]

    action = questionary.select("Upgrade options:", choices=choices, style=CUSTOM_STYLE).ask()
    if action == "all":
        cmd = ["winget", "upgrade", "--all", "--accept-package-agreements", "--accept-source-agreements", "--disable-interactivity"]
        subprocess.run(cmd)
        scan_installed_apps(force_refresh=True)
        questionary.press_any_key_to_continue().ask()

    elif action == "select":
        app_choices = [
            Choice(f"{u['name']} ({u['version']} -> {u['available']})", value=u["id"], checked=True)
            for u in upgrades
        ]
        chosen_ids = questionary.checkbox("Select apps to upgrade:", choices=app_choices, style=CUSTOM_STYLE).ask()
        if chosen_ids:
            for pkg_id in chosen_ids:
                CONSOLE.print(f"\n[cyan]Upgrading {pkg_id}...[/cyan]")
                subprocess.run(["winget", "upgrade", "--id", pkg_id, "--accept-package-agreements", "--accept-source-agreements", "--disable-interactivity"])
            scan_installed_apps(force_refresh=True)
            CONSOLE.print("[bold green][✓] Selected upgrades completed![/bold green]")
            questionary.press_any_key_to_continue().ask()

def handle_shell_booster_menu():
    """Handle PowerShell Profile & Starship quick optimizer."""
    print_banner()
    CONSOLE.print("[bold cyan]=== ⚡ Terminal & PowerShell Quick-Booster ===[/bold cyan]\n")
    CONSOLE.print(
        "This booster will automatically configure your PowerShell profile with:\n"
        "  • [bold green]PSReadLine Predictive IntelliSense[/bold green] (Fish-shell style suggestions)\n"
        "  • [bold green]Starship Prompt Integration[/bold green]\n"
        "  • [bold green]UTF-8 Output Encoding[/bold green]\n"
        "  • [bold green]Power-User Aliases[/bold green] (ll, grep, which, touch, reload-profile)\n"
    )

    confirm = questionary.confirm("Apply modern PowerShell profile configuration?", default=True).ask()
    if not confirm:
        return

    # Check if starship is installed
    has_starship = shutil.which("starship") is not None
    if not has_starship:
        install_starship = questionary.confirm("Starship prompt is not detected. Would you like to install Starship via Winget now?", default=True).ask()
        if install_starship:
            CONSOLE.print("[cyan]Installing Starship.Starship...[/cyan]")
            subprocess.run(["winget", "install", "Starship.Starship", "-e", "--accept-package-agreements", "--accept-source-agreements"])

    res = shell_booster.setup_powershell_profile()
    if res["success"]:
        CONSOLE.print("\n[bold green][✓] PowerShell Profile configured successfully at:[/bold green]")
        for p in res["configured_paths"]:
            CONSOLE.print(f"  • {p}")
        CONSOLE.print("\n[dim]To test the new features, open a new PowerShell window or run 'reload-profile'.[/dim]")
    else:
        CONSOLE.print(f"[bold red]Failed to configure profiles: {res['errors']}[/bold red]")

    questionary.press_any_key_to_continue().ask()

def handle_preflight_check():
    """System Pre-Flight Health & Disk Space Check."""
    print_banner()
    CONSOLE.print("[bold cyan]=== 🩺 System Pre-Flight & Health Check ===[/bold cyan]\n")

    # 1. Disk Space Check
    try:
        usage = shutil.disk_usage("C:\\")
        total_gb = usage.total / (1024 ** 3)
        free_gb = usage.free / (1024 ** 3)
        used_gb = usage.used / (1024 ** 3)
        disk_status = f"[green]{free_gb:.1f} GB Free[/green] / {total_gb:.1f} GB Total ({used_gb:.1f} GB Used)"
    except Exception:
        disk_status = "[yellow]Could not determine C:\\ disk usage[/yellow]"

    # 2. Admin Privileges
    admin_str = "[bold green]✓ Elevated (Administrator)[/bold green]" if is_admin() else "[yellow]⚠ Standard User (Run as Admin recommended)[/yellow]"

    # 3. Winget CLI Health
    winget_path = shutil.which("winget")
    if winget_path:
        try:
            ver_res = subprocess.run(["winget", "--version"], stdout=subprocess.PIPE, text=True, timeout=5)
            winget_status = f"[bold green]✓ Available (v{ver_res.stdout.strip()})[/bold green]"
        except Exception:
            winget_status = "[bold green]✓ Available[/bold green]"
    else:
        winget_status = "[bold red]✗ Not Found[/bold red]"

    # 4. Internet Connectivity
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        net_status = "[bold green]✓ Connected (Internet reachable)[/bold green]"
    except Exception:
        net_status = "[bold red]✗ No Internet Connection detected[/bold red]"

    # 5. Winget CDN Reachability
    try:
        req = urllib.request.Request("https://cdn.winget.microsoft.com", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=4) as response:
            cdn_status = "[bold green]✓ Reachable[/bold green]"
    except Exception:
        cdn_status = "[yellow]⚠ CDN ping skipped or slow[/yellow]"

    table = Table(show_header=True, header_style="bold cyan", title="System Health Summary")
    table.add_column("Component / Check", style="bold white", width=30)
    table.add_column("Status / Details", width=45)

    table.add_row("🛡️ Privilege Level", admin_str)
    table.add_row("💾 Drive C: Storage", disk_status)
    table.add_row("📦 Winget CLI", winget_status)
    table.add_row("🌐 Internet Connection", net_status)
    table.add_row("🚀 Winget CDN Service", cdn_status)

    CONSOLE.print(table)
    CONSOLE.print("\n[dim]Everything is ready for optimal package installation and system configuration.[/dim]\n")
    questionary.press_any_key_to_continue().ask()

def handle_presets_menu(apps: List[Dict[str, Any]], installed_set: Set[str]):
    """Handle selecting and running curated Persona Presets."""
    presets = load_presets()
    if not presets:
        CONSOLE.print("[bold red]No presets found in presets.json[/bold red]")
        questionary.press_any_key_to_continue().ask()
        return

    preset_choices = []
    for key, pdata in presets.items():
        preset_choices.append(Choice(
            title=f"{pdata['name']} - [dim]{pdata['description']}[/dim]",
            value=key
        ))
    preset_choices.append(Choice("← Back", value="back"))

    chosen_key = questionary.select("Select Persona Preset:", choices=preset_choices, style=CUSTOM_STYLE).ask()
    if chosen_key == "back" or chosen_key is None:
        return

    preset = presets[chosen_key]
    target_ids = set(preset.get("app_ids", []))

    choices = build_choices(apps, target_ids=target_ids, installed_set=installed_set)
    selected = questionary.checkbox(
        f"Review & Confirm [{preset['name']}]:",
        choices=choices,
        instruction="(Space: toggle, Enter: confirm, Ctrl+C: cancel)",
        style=CUSTOM_STYLE
    ).ask()

    if selected is not None:
        execute_installation(selected)

def handle_custom_profiles_menu(apps: List[Dict[str, Any]], installed_set: Set[str]):
    """Handle saving and loading custom user profiles."""
    profiles = load_custom_profiles()
    sub_choices = [
        Choice("💾 Save New Profile from Checkbox Selection", value="save"),
        Choice("📂 Load & Install Existing Profile", value="load"),
        Choice("← Back", value="back")
    ]

    action = questionary.select("Custom Profiles:", choices=sub_choices, style=CUSTOM_STYLE).ask()
    if action == "save":
        pname = questionary.text("Enter Profile Name (e.g. Work Laptop, Gaming Rig):").ask()
        if not pname:
            return

        choices = build_choices(apps, installed_set=installed_set)
        selected = questionary.checkbox(
            f"Select applications to include in profile '{pname}':",
            choices=choices,
            style=CUSTOM_STYLE
        ).ask()

        if selected is not None and len(selected) > 0:
            profiles[pname] = [app["id"] for app in selected]
            if save_custom_profiles(profiles):
                CONSOLE.print(f"[bold green][✓] Profile '{pname}' saved with {len(selected)} apps![/bold green]")
        questionary.press_any_key_to_continue().ask()

    elif action == "load":
        if not profiles:
            CONSOLE.print("[yellow]No custom profiles saved yet.[/yellow]")
            questionary.press_any_key_to_continue().ask()
            return

        p_choices = [Choice(name, value=name) for name in profiles.keys()] + [Choice("← Back", value="back")]
        chosen_profile = questionary.select("Select Profile to Load:", choices=p_choices, style=CUSTOM_STYLE).ask()

        if chosen_profile and chosen_profile != "back":
            target_ids = set(profiles[chosen_profile])
            choices = build_choices(apps, target_ids=target_ids, installed_set=installed_set)
            selected = questionary.checkbox(
                f"Review & Install profile [{chosen_profile}]:",
                choices=choices,
                style=CUSTOM_STYLE
            ).ask()
            if selected is not None:
                execute_installation(selected)

def handle_tweaks_menu():
    """Handle Windows System & Explorer Tweaks with Rollback."""
    print_banner()
    CONSOLE.print("[bold cyan]=== 🛠️ Windows System & Explorer Tweaks ===[/bold cyan]\n")

    tweak_mode = questionary.select(
        "Tweaks Options:",
        choices=[
            Choice("⚡ Apply Windows Optimizations & Tweaks", value="apply"),
            Choice("↩️ Revert / Rollback Tweaks to Defaults", value="revert"),
            Choice("← Back", value="back")
        ],
        style=CUSTOM_STYLE
    ).ask()

    if tweak_mode == "back" or tweak_mode is None:
        return

    if tweak_mode == "apply":
        tweak_choices = []
        for t in tweaks.TWEAKS_LIST:
            display_title = f"{t['name']} - [dim]{t['description']}[/dim]"
            tweak_choices.append(Choice(
                title=display_title,
                value=t["id"],
                checked=t.get("default", False)
            ))

        selected_ids = questionary.checkbox(
            "Select Tweaks to apply to Windows:",
            choices=tweak_choices,
            instruction="(Space: toggle, Enter: apply, Ctrl+C: back)",
            style=CUSTOM_STYLE
        ).ask()

        if selected_ids:
            results = tweaks.apply_selected_tweaks(selected_ids)
            CONSOLE.print("\n[bold cyan]Tweaks Application Results:[/bold cyan]")
            for r in results:
                status = "[green][✓] Applied[/green]" if r["success"] else "[red][✗] Failed (Admin required)[/red]"
                CONSOLE.print(f"  {status} {r['name']}")

            restart = questionary.confirm("Restart Windows Explorer now to apply visual changes?", default=True).ask()
            if restart:
                tweaks.restart_explorer()
                CONSOLE.print("[bold green][✓] Windows Explorer restarted successfully![/bold green]")
            questionary.press_any_key_to_continue().ask()

    elif tweak_mode == "revert":
        tweak_choices = []
        for t in tweaks.TWEAKS_LIST:
            display_title = f"{t['name']} - [dim]{t['description']}[/dim]"
            tweak_choices.append(Choice(
                title=display_title,
                value=t["id"],
                checked=True
            ))

        selected_ids = questionary.checkbox(
            "Select Tweaks to revert back to default state:",
            choices=tweak_choices,
            style=CUSTOM_STYLE
        ).ask()

        if selected_ids:
            results = tweaks.revert_selected_tweaks(selected_ids)
            CONSOLE.print("\n[bold cyan]Tweaks Rollback Results:[/bold cyan]")
            for r in results:
                status = "[green][✓] Reverted[/green]" if r["success"] else "[red][✗] Failed[/red]"
                CONSOLE.print(f"  {status} {r['name']}")

            restart = questionary.confirm("Restart Windows Explorer now to apply reverted changes?", default=True).ask()
            if restart:
                tweaks.restart_explorer()
                CONSOLE.print("[bold green][✓] Windows Explorer restarted successfully![/bold green]")
            questionary.press_any_key_to_continue().ask()

def add_new_app_interactive(apps: List[Dict[str, Any]]):
    """Prompt user to add a new app directly to apps.json."""
    print_banner()
    CONSOLE.print("[bold yellow]=== ➕ Add New Application ===[/bold yellow]\n")

    name = questionary.text("App Display Name (e.g. VLC Media Player):").ask()
    if not name:
        return

    app_id = questionary.text("Winget Package ID (e.g. VideoLAN.VLC):").ask()
    if not app_id:
        return

    existing_categories = sorted(list(set(app.get("category", "Other") for app in apps)))
    category_choices = existing_categories + ["[+ Add New Category]"]
    chosen_cat = questionary.select("Select Category:", choices=category_choices, style=CUSTOM_STYLE).ask()

    if chosen_cat == "[+ Add New Category]":
        category = questionary.text("Enter New Category Name:").ask()
        if not category:
            category = "Other"
    else:
        category = chosen_cat

    description = questionary.text("Description / Notes (optional):").ask() or ""
    default_checked = questionary.confirm("Check by default in TUI?", default=True).ask()

    new_entry = {
        "category": category,
        "name": name,
        "id": app_id,
        "description": description,
        "default": bool(default_checked)
    }

    apps.append(new_entry)
    if save_apps(apps):
        CONSOLE.print(f"[bold green][✓] Added '{name}' ({app_id}) to apps.json![/bold green]")
    questionary.press_any_key_to_continue().ask()

def main_menu():
    """Main interactive loop."""
    if not check_winget():
        print_banner()
        CONSOLE.print(
            "[bold red][!] Winget is not installed or not found in PATH.[/bold red]\n"
            "Please ensure Windows App Installer is installed from the Microsoft Store or updated."
        )
        sys.exit(1)

    # Initial scan of installed applications
    installed_set = scan_installed_apps()

    while True:
        print_banner()
        apps = load_apps()
        if not apps:
            CONSOLE.print("[bold red]No apps configured in apps.json.[/bold red]")
            break

        total_apps = len(apps)
        categories = sorted(list(set(app.get("category", "General") for app in apps)))

        CONSOLE.print(f"[dim]Loaded {total_apps} apps across {len(categories)} categories | Detected {len(installed_set)} installed packages.[/dim]\n")

        menu_choices = [
            Choice("🚀 Select & Install Apps (Full Checkbox TUI)", value="select_all"),
            Choice("🎯 Curated Persona Presets (Dev, Gamer, Creator, Minimalist...)", value="presets"),
            Choice("📂 Filter & Select by Category", value="by_category"),
            Choice("🔍 Live In-App Winget Search (Find & Install on the fly)", value="search"),
            Choice("📊 Interactive Updates Dashboard (Installed vs Latest)", value="upgrade_dash"),
            Choice("🧹 Windows Bloatware Remover (Debloater)", value="debloat"),
            Choice("🛠️ Windows System & Explorer Tweaks (with Rollback)", value="tweaks"),
            Choice("⚡ Boost PowerShell & Terminal (Starship, Aliases & IntelliSense)", value="shell_booster"),
            Choice("💾 PC Setup Migration (Backup & Restore Software Inventory)", value="migration"),
            Choice("🩺 System Pre-Flight & Health Check", value="preflight"),
            Choice("💾 Custom Profiles (Save / Load Custom App Bundles)", value="custom_profiles"),
            Choice("➕ Add New App to apps.json", value="add_app"),
            Choice("📝 Open apps.json in Default Text Editor", value="edit_json"),
            Choice("❌ Exit", value="exit")
        ]

        action = questionary.select(
            "What would you like to do?",
            choices=menu_choices,
            style=CUSTOM_STYLE
        ).ask()

        if action == "exit" or action is None:
            CONSOLE.print("[bold cyan]Goodbye![/bold cyan]")
            break

        elif action == "select_all":
            choices = build_choices(apps, installed_set=installed_set)
            instruction_text = "(Space to select/deselect, 'a' to toggle all, 'i' to invert, Enter to confirm)"
            selected = questionary.checkbox(
                "Select applications to install:",
                choices=choices,
                instruction=instruction_text,
                style=CUSTOM_STYLE
            ).ask()

            if selected is not None:
                execute_installation(selected)
                installed_set = scan_installed_apps(force_refresh=True)

        elif action == "presets":
            handle_presets_menu(apps, installed_set)
            installed_set = scan_installed_apps(force_refresh=True)

        elif action == "by_category":
            cat_choices = categories + ["← Back"]
            chosen_cat = questionary.select(
                "Choose Category to Install:",
                choices=cat_choices,
                style=CUSTOM_STYLE
            ).ask()

            if chosen_cat and chosen_cat != "← Back":
                choices = build_choices(apps, filter_cat=chosen_cat, installed_set=installed_set)
                selected = questionary.checkbox(
                    f"Select applications in [{chosen_cat}]:",
                    choices=choices,
                    instruction="(Space: toggle, Enter: confirm)",
                    style=CUSTOM_STYLE
                ).ask()
                if selected is not None:
                    execute_installation(selected)
                    installed_set = scan_installed_apps(force_refresh=True)

        elif action == "search":
            handle_winget_search_menu(apps)
            installed_set = scan_installed_apps(force_refresh=True)

        elif action == "upgrade_dash":
            handle_upgrade_dashboard()
            installed_set = scan_installed_apps(force_refresh=True)

        elif action == "debloat":
            handle_debloat_menu()

        elif action == "tweaks":
            handle_tweaks_menu()

        elif action == "shell_booster":
            handle_shell_booster_menu()

        elif action == "migration":
            handle_migration_menu(apps, installed_set)
            installed_set = scan_installed_apps(force_refresh=True)

        elif action == "preflight":
            handle_preflight_check()

        elif action == "custom_profiles":
            handle_custom_profiles_menu(apps, installed_set)
            installed_set = scan_installed_apps(force_refresh=True)

        elif action == "add_app":
            add_new_app_interactive(apps)

        elif action == "edit_json":
            try:
                os.startfile(APPS_FILE)
                CONSOLE.print(f"[green][✓] Opened {APPS_FILE} in default editor.[/green]")
            except Exception as e:
                CONSOLE.print(f"[red]Could not open editor: {e}[/red]")
            questionary.press_any_key_to_continue().ask()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        CONSOLE.print("\n[yellow]Operation canceled by user.[/yellow]")
        sys.exit(0)
