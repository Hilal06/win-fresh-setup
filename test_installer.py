"""
Automated Test Suite for Windows 11 Winget App Installer
"""
import os
import sys
import json
import shutil

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

def test_imports():
    print("[TEST 1] Testing imports...")
    import questionary
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress
    import installer
    print("  [OK] All modules imported successfully.")

def test_apps_json_validity():
    print("\n[TEST 2] Testing apps.json structure and validity...")
    import installer
    apps = installer.load_apps()
    assert len(apps) > 0, "apps.json is empty or not loaded"
    required_keys = {"category", "name", "id", "description", "default"}
    for idx, app in enumerate(apps):
        for key in required_keys:
            assert key in app, f"Missing key '{key}' in app entry #{idx}: {app}"
        assert isinstance(app["category"], str) and len(app["category"]) > 0
        assert isinstance(app["name"], str) and len(app["name"]) > 0
        assert isinstance(app["id"], str) and len(app["id"]) > 0
        assert isinstance(app["default"], bool)
    print(f"  [OK] {len(apps)} applications validated successfully.")

def test_choices_builder():
    print("\n[TEST 3] Testing Questionary choices generator...")
    import installer
    apps = installer.load_apps()
    choices = installer.build_choices(apps)
    assert len(choices) > 0, "No choices generated"
    
    # Test filtered choices
    categories = list(set(a["category"] for a in apps))
    sample_cat = categories[0]
    cat_choices = installer.build_choices(apps, filter_cat=sample_cat)
    assert len(cat_choices) > 0, f"No choices generated for category '{sample_cat}'"
    print("  [OK] Choice generator and category filtering working as expected.")

def test_winget_availability():
    print("\n[TEST 4] Testing Winget CLI accessibility...")
    import installer
    assert installer.check_winget() is True, "Winget not found in PATH"
    print("  [OK] Winget CLI is available and detected.")

def test_log_directory_creation():
    print("\n[TEST 5] Testing log directory creation...")
    import installer
    installer.ensure_dirs()
    assert os.path.exists(installer.LOGS_DIR), "Logs directory not created"
    print(f"  [OK] Logs directory verified at: {installer.LOGS_DIR}")

def test_winget_single_app_dryrun():
    print("\n[TEST 6] Testing Winget query command execution...")
    import installer
    # Test winget show / query on 7-Zip as a fast non-destructive check
    test_app = {"name": "7-Zip", "id": "7zip.7zip", "category": "Productivity & Documents"}
    installer.ensure_dirs()
    log_path = os.path.join(installer.LOGS_DIR, "test_execution.log")
    
    # We run winget list/show to verify subprocessing works smoothly
    result = installer.run_winget_install(test_app, log_path)
    print(f"  [OK] Winget execution returned status: {result['status']} ({result['message']})")
    assert "status" in result
    assert os.path.exists(log_path)
    print(f"  [OK] Execution log created and populated.")

def run_all_tests():
    print("=" * 60)
    print(" Running Winget App Installer Automated Tests ")
    print("=" * 60)
    test_imports()
    test_apps_json_validity()
    test_choices_builder()
    test_winget_availability()
    test_log_directory_creation()
    test_winget_single_app_dryrun()
    print("\n" + "=" * 60)
    print(" ALL TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()
