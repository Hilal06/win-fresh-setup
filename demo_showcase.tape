# VHS Tape Showcase untuk win-fresh-setup
# Menghasilkan animasi GIF walkthrough TUI asli ke demo/win-fresh-setup-showcase.gif

Output "demo/win-fresh-setup-showcase.gif"

# Konfigurasi Shell untuk Windows Terminal Modern
Set Shell "pwsh"

Set FontSize 14
Set Width 1280
Set Height 820
Set Padding 16
Set WindowBar Colorful
Set Margin 20
Set Theme "Catppuccin Mocha"

# 1. Mulai TUI Showcase Runner
Type ".\.venv\Scripts\python.exe demo/vhs_runner.py"
Enter
Sleep 3s

# 2. Main Menu: Masuk ke Fitur 'Install Applications'
Enter
Sleep 2.5s

# 3. Interaksi Checkbox [X] dan [ ]
Down
Sleep 600ms
Space
Sleep 600ms
Down
Sleep 600ms
Space
Sleep 1s

# 4. Konfirmasi Seleksi Aplikasi
Enter
Sleep 1.5s

# 5. Konfirmasi Mulai Instalasi
Enter

# 6. Animasi Live Progress Bar & Spinner
Sleep 3.5s

# 7. Tampilan Laporan Ringkasan Hasil Instalasi
Sleep 1.5s
Enter
Sleep 2s

# 8. Navigasi ke Curated Persona Presets
Down
Sleep 800ms
Enter
Sleep 2.5s

# 9. Kembali ke Main Menu
Down 5
Sleep 600ms
Enter
Sleep 2s

# 10. Navigasi ke System Pre-Flight Health Check
Down 9
Sleep 800ms
Enter
Sleep 3s

# 11. Kembali ke Menu Utama dan Exit
Enter
Sleep 1.5s
Up
Sleep 800ms
Enter
Sleep 2s
