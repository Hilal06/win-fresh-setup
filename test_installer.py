"""
Automated Test Suite for win-fresh-setup
Comprehensive tests for Apps, Presets, Tweaks, Debloater, Shell Booster, and Parsers.
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
    import tweaks
    import debloat
    import shell_booster
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

def test_presets_json_validity():
    print("\n[TEST 3] Testing presets.json structure and validity...")
    import installer
    presets = installer.load_presets()
    assert len(presets) > 0, "presets.json is empty or not loaded"
    apps = installer.load_apps()
    valid_ids = {a["id"] for a in apps}
    
    for key, preset in presets.items():
        assert "name" in preset, f"Preset '{key}' missing 'name'"
        assert "description" in preset, f"Preset '{key}' missing 'description'"
        assert "app_ids" in preset and isinstance(preset["app_ids"], list), f"Preset '{key}' missing 'app_ids' list"
        for app_id in preset["app_ids"]:
            assert app_id in valid_ids, f"Preset '{key}' references unknown app ID: '{app_id}'"
    print(f"  [OK] {len(presets)} preset profiles validated successfully.")

def test_tweaks_module():
    print("\n[TEST 4] Testing tweaks.py structure & backup capabilities...")
    import tweaks
    assert len(tweaks.TWEAKS_LIST) > 0, "No tweaks defined in tweaks.py"
    for tweak in tweaks.TWEAKS_LIST:
        assert "id" in tweak
        assert "name" in tweak
        assert "description" in tweak
        assert "actions" in tweak and len(tweak["actions"]) > 0

    # Test backup trigger
    backup_file = tweaks.backup_current_tweaks(["dark_mode", "show_file_ext"])
    if backup_file:
        assert os.path.exists(backup_file), "Backup file was not created"
        print(f"  [OK] Tweaks backup file verified at: {backup_file}")
    print(f"  [OK] {len(tweaks.TWEAKS_LIST)} registry tweaks validated successfully.")

def test_debloat_module():
    print("\n[TEST 5] Testing debloat.py structure...")
    import debloat
    assert len(debloat.DEBLOAT_LIST) > 0, "No debloat packages defined"
    for item in debloat.DEBLOAT_LIST:
        assert "id" in item
        assert "name" in item
        assert "description" in item
        assert "default" in item
    print(f"  [OK] {len(debloat.DEBLOAT_LIST)} bloatware definitions validated successfully.")

def test_shell_booster_module():
    print("\n[TEST 6] Testing shell_booster.py paths and content...")
    import shell_booster
    paths = shell_booster.get_powershell_profile_paths()
    assert len(paths) > 0, "No profile paths generated"
    assert len(shell_booster.MODERN_PROFILE_CONTENT) > 50
    print(f"  [OK] Shell booster profile generation verified.")

def test_winget_table_parser():
    print("\n[TEST 7] Testing fixed-width Winget output parser...")
    import installer
    sample = (
        "Name                            Id                            Version       Available      Source\n"
        "-------------------------------------------------------------------------------------------------\n"
        "EaseUS Partition Master         EaseUS.PartitionMaster        19.9          2080           winget\n"
        "LocalSend version 1.17.0        LocalSend.LocalSend           1.17.0        1.18.2         winget\n"
        "2 upgrades available.\n"
    )
    parsed = installer.parse_winget_table(sample)
    assert len(parsed) == 2, f"Expected 2 parsed entries, got {len(parsed)}"
    assert parsed[0]["id"] == "EaseUS.PartitionMaster"
    assert parsed[0]["version"] == "19.9"
    assert parsed[0]["available"] == "2080"
    assert parsed[1]["id"] == "LocalSend.LocalSend"
    print("  [OK] Winget table parser verified successfully.")

def test_title_loading():
    print("\n[TEST 8] Testing title.txt loading...")
    import installer
    title = installer.load_title()
    assert len(title) > 0, "Title art is empty"
    print("  [OK] Title ASCII art loaded successfully.")

def test_choices_builder():
    print("\n[TEST 9] Testing Questionary choices generator...")
    import installer
    apps = installer.load_apps()
    choices = installer.build_choices(apps)
    assert len(choices) > 0, "No choices generated"
    
    categories = list(set(a["category"] for a in apps))
    sample_cat = categories[0]
    cat_choices = installer.build_choices(apps, filter_cat=sample_cat)
    assert len(cat_choices) > 0, f"No choices generated for category '{sample_cat}'"
    print("  [OK] Choice generator and category filtering working as expected.")

def test_winget_availability():
    print("\n[TEST 10] Testing Winget CLI accessibility...")
    import installer
    is_available = installer.check_winget()
    if is_available:
        print("  [OK] Winget CLI is available and detected.")
    else:
        print("  [WARN] Winget CLI not found in current environment (Expected on GitHub Actions runner).")

def test_log_directory_creation():
    print("\n[TEST 11] Testing log directory creation...")
    import installer
    installer.ensure_dirs()
    assert os.path.exists(installer.LOGS_DIR), "Logs directory not created"
    print(f"  [OK] Logs directory verified at: {installer.LOGS_DIR}")

def run_all_tests():
    print("=" * 60)
    print(" Running win-fresh-setup Automated Test Suite ")
    print("=" * 60)
    test_imports()
    test_apps_json_validity()
    test_presets_json_validity()
    test_tweaks_module()
    test_debloat_module()
    test_shell_booster_module()
    test_winget_table_parser()
    test_title_loading()
    test_choices_builder()
    test_winget_availability()
    test_log_directory_creation()
    print("\n" + "=" * 60)
    print(" ALL 11 TEST SUITES PASSED SUCCESSFULLY! ")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()
