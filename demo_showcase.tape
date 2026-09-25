# VHS Tape Showcase untuk win-fresh-setup
# Menghasilkan animasi GIF dan screenshot PNG per fitur ke folder demo/

Output "demo/win-fresh-setup-showcase.gif"

Set Shell "bash"
Set FontSize 14
Set Width 1280
Set Height 800
Set Padding 16
Set WindowBar Colorful
Set Margin 20
Set Theme "Catppuccin Mocha"

# Jalankan Python installer di dalam Git bash
Type "python installer.py"
Enter

# Tunggu pemindaian awal selesai dan layar prompt hak akses/menu tampil
Sleep 4s

# 1. Screenshot: Pemberitahuan Hak Akses Administrator
Screenshot "demo/01_elevation_prompt.png"
Sleep 1s

# Navigasi ke opsi "👤 Tetap Lanjut sebagai Standard User"
Down
Sleep 600ms
Enter

# Tunggu banner & main menu termuat penuh
Sleep 3.5s

# 2. Screenshot: Menu Utama TUI
Screenshot "demo/02_main_menu.png"
Sleep 1s

# 3. Screenshot: Fitur Select & Install Apps (Full Checkbox TUI)
Enter
Sleep 2s
Screenshot "demo/03_select_install_apps.png"
# Tekan Escape lalu batalkan kembali ke menu utama
Ctrl+C
Sleep 2s

# 4. Screenshot: Fitur Curated Persona Presets
Down
Sleep 600ms
Enter
Sleep 2s
Screenshot "demo/04_persona_presets.png"
Ctrl+C
Sleep 2s

# 5. Screenshot: Fitur Filter by Category
Down 2
Sleep 600ms
Enter
Sleep 2s
Screenshot "demo/05_filter_by_category.png"
Ctrl+C
Sleep 2s

# 6. Screenshot: Fitur Windows Bloatware Remover (Debloater)
Down 5
Sleep 600ms
Enter
Sleep 2s
Screenshot "demo/06_bloatware_remover.png"
Ctrl+C
Sleep 2s

# 7. Screenshot: Fitur Windows System & Explorer Tweaks
Down 6
Sleep 600ms
Enter
Sleep 2s
Screenshot "demo/07_system_tweaks.png"
Ctrl+C
Sleep 2s

# 8. Screenshot: Fitur Boost PowerShell & Terminal
Down 7
Sleep 600ms
Enter
Sleep 2s
Screenshot "demo/08_powershell_booster.png"
Ctrl+C
Sleep 2s

# 9. Screenshot: Fitur System Pre-Flight & Health Check
Down 9
Sleep 600ms
Enter
Sleep 3s
Screenshot "demo/09_system_health_check.png"
Enter
Sleep 2s

# Selesai: Sorot opsi Exit dan akhiri sesi
Down 13
Sleep 600ms
Screenshot "demo/10_exit_menu.png"
Enter
Sleep 2s
