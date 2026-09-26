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

# 1. Simulate Elevated Administrator Session in memory (no UAC prompt pop-up)
installer.is_admin = lambda: True

# 2. Instant pre-cached installed applications for realistic badge rendering
MOCK_INSTALLED = {
    "mozilla.firefox",
    "google.chrome",
    "git.git",
    "openjs.nodejs.lts"
}
installer.scan_installed_apps = lambda force_refresh=False: set(MOCK_INSTALLED)

# 3. Simulated realistic Winget installation queue with live progress
def simulated_winget_install(app, log_file_path):
    """Simulate rapid visual installation for recording demos."""
    time.sleep(0.7)
    with open(log_file_path, "a", encoding="utf-8") as f:
        f.write(f"Simulated install for {app['name']} ({app['id']})\n")
    return {"status": "SUCCESS", "message": "Installed successfully"}

installer.run_winget_install = simulated_winget_install

if __name__ == "__main__":
    installer.ensure_dirs()
    installer.main_menu()
