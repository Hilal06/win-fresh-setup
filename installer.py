#!/usr/bin/env python3
"""
Windows 11 Winget Automation & TUI App Installer
Author: Rifaul06

Features:
- Interactive TUI multi-select with search and categories (via questionary & rich)
- Fully customizable external apps.json configuration
- Live installation progress and error detection
- Summary table and persistent installation logging
"""

import sys
import os
import json
import subprocess
import shutil
from datetime import datetime
from typing import List, Dict, Any, Optional

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
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.prompt import Confirm
    from rich import print as rprint
except ImportError:
    print("[!] Missing required packages. Please install requirements:")
    print("    pip install -r requirements.txt")
    sys.exit(1)

CONSOLE = Console()
APPS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apps.json")
LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")

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

def ensure_dirs():
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR, exist_ok=True)

def print_banner():
    CONSOLE.clear()
    banner_text = (
        "[bold cyan]Windows 11 Winget App Installer[/bold cyan]\n"
        "[dim]Automated Package Installer & Management TUI[/dim]\n"
        "[italic magenta]Developed by Rifaul06[/italic magenta]"
    )
    CONSOLE.print(Panel(banner_text, border_style="cyan", expand=False))

def check_winget() -> bool:
    """Check if winget CLI is accessible."""
    return shutil.which("winget") is not None

def load_apps() -> List[Dict[str, Any]]:
    """Load application list from apps.json."""
    if not os.path.exists(APPS_FILE):
        CONSOLE.print(f"[bold red][!] Config file not found:[/bold red] {APPS_FILE}")
        return []
    try:
        with open(APPS_FILE, "r", encoding="utf-8") as f:
            apps = json.load(f)
            return apps
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

def add_new_app_interactive(apps: List[Dict[str, Any]]):
    """Prompt user to add a new app directly to apps.json."""
    print_banner()
    CONSOLE.print("[bold yellow]=== Add New Application ===[/bold yellow]\n")

    name = questionary.text("App Display Name (e.g. VLC Media Player):").ask()
    if not name:
        return

    app_id = questionary.text("Winget Package ID (e.g. VideoLAN.VLC):").ask()
    if not app_id:
        return

    # Offer existing categories or custom
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

def build_choices(apps: List[Dict[str, Any]], filter_cat: Optional[str] = None) -> List[Any]:
    """Construct Questionary choice list grouped with category separators."""
    # Group by category
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
            display_title = f"{app['name']} [dim]({app['id']})[/dim]"
            if app.get("description"):
                display_title += f" - {app['description']}"
            
            choices.append(Choice(
                title=display_title,
                value=app,
                checked=app.get("default", False)
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

            # Analyze return code and output
            # Winget exit codes:
            # 0: Success
            # -1978335189 / 0x8A15002B: Already installed
            # -1978335212: No package found
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
    """Run sequential installation of selected packages with live rich progress."""
    if not selected_apps:
        CONSOLE.print("[bold yellow]No applications selected.[/bold yellow]")
        questionary.press_any_key_to_continue().ask()
        return

    ensure_dirs()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_path = os.path.join(LOGS_DIR, f"winget_install_{timestamp}.log")

    print_banner()
    # Review selection table
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

            # Live notification per app
            if res["status"] == "SUCCESS":
                CONSOLE.print(f"  [bold green][✓] {app['name']}[/bold green] - Installed successfully")
            elif res["status"] == "ALREADY_INSTALLED":
                CONSOLE.print(f"  [bold yellow][i] {app['name']}[/bold yellow] - Already installed")
            elif res["status"] == "NOT_FOUND":
                CONSOLE.print(f"  [bold red][✗] {app['name']}[/bold red] - Package ID not found ({app['id']})")
            else:
                CONSOLE.print(f"  [bold red][✗] {app['name']}[/bold red] - Failed: {res['message']}")

            progress.advance(overall_task)

    # Final Summary Table
    CONSOLE.print("\n")
    summary_table = Table(title="Installation Summary Report", show_header=True, header_style="bold cyan")
    summary_table.add_column("App Name", style="bold white", width=25)
    summary_table.add_column("Winget ID", style="dim", width=28)
    summary_table.add_column("Status", width=18)
    summary_table.add_column("Details", width=35)

    success_cnt = 0
    already_cnt = 0
    failed_cnt = 0

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
            failed_cnt += 1

        summary_table.add_row(app["name"], app["id"], status_str, r["message"])

    CONSOLE.print(summary_table)

    CONSOLE.print(
        f"\n[bold]Results:[/bold] "
        f"[green]{success_cnt} Installed[/green] | "
        f"[yellow]{already_cnt} Already Present[/yellow] | "
        f"[red]{failed_cnt} Failed[/red]"
    )
    CONSOLE.print(f"[dim]Full logs saved to: {log_file_path}[/dim]\n")
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

    while True:
        print_banner()
        apps = load_apps()
        if not apps:
            CONSOLE.print("[bold red]No apps configured in apps.json.[/bold red]")
            break

        total_apps = len(apps)
        categories = sorted(list(set(app.get("category", "General") for app in apps)))

        CONSOLE.print(f"[dim]Loaded {total_apps} apps across {len(categories)} categories.[/dim]\n")

        menu_choices = [
            Choice("🚀 Select & Install Apps (Full Interactive Checkbox TUI)", value="select_all"),
            Choice("📂 Filter & Select by Category", value="by_category"),
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
            choices = build_choices(apps)
            instruction_text = "(Space to select/deselect, 'a' to toggle all, 'i' to invert, Enter to confirm)"
            selected = questionary.checkbox(
                "Select applications to install:",
                choices=choices,
                instruction=instruction_text,
                style=CUSTOM_STYLE
            ).ask()

            if selected is not None:
                execute_installation(selected)

        elif action == "by_category":
            cat_choices = categories + ["← Back"]
            chosen_cat = questionary.select(
                "Choose Category to Install:",
                choices=cat_choices,
                style=CUSTOM_STYLE
            ).ask()

            if chosen_cat and chosen_cat != "← Back":
                choices = build_choices(apps, filter_cat=chosen_cat)
                selected = questionary.checkbox(
                    f"Select applications in [{chosen_cat}]:",
                    choices=choices,
                    instruction="(Space: toggle, Enter: confirm)",
                    style=CUSTOM_STYLE
                ).ask()
                if selected is not None:
                    execute_installation(selected)

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
