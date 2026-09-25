# Project Rules: win-fresh-setup

Panduan dan batasan pengerjaan kode untuk proyek `win-fresh-setup`.

## 1. Lingkungan & Bahasa Pemrograman
- **Python**: Versi target 3.10+ di Windows.
- **Dependencies**: Menggunakan `rich` dan `questionary`. Jangan menambahkan dependensi eksternal berat baru tanpa pertimbangan matang.
- **Encoding**: Selalu pastikan stdout/stderr dikonfigurasi dengan encoding `utf-8` (`sys.stdout.reconfigure(encoding="utf-8")`) agar kompatibel dengan Windows Terminal & PowerShell/CMD.

## 2. Struktur Data `apps.json` & `presets.json`
- Setiap entri di `apps.json` **wajib** memiliki 5 properti:
  - `category` (string, tidak boleh kosong)
  - `name` (string nama aplikasi)
  - `id` (string Winget ID yang valid atau Store ID 12 karakter)
  - `description` (ringkasan fungsi)
  - `default` (boolean: `true`/`false`)
- Setiap `id` baru di `apps.json` harus dipastikan unik (tidak boleh duplikat).
- Di `presets.json`, setiap entri pada array `app_ids` **harus** merujuk pada `id` yang sudah terdaftar di `apps.json`.

## 3. Registry & System Tweaks (`tweaks.py`)
- Setiap modifikasi registry Windows **wajib** memiliki mekanisme pencadangan (*backup*) nilai lama sebelum diubah.
- Setiap tweak harus memiliki fungsi `revert` atau `rollback` yang setara.
- Gunakan try-except saat mengakses `winreg` untuk menangani skenario tanpa akses Administrator.

## 4. Debloater & PowerShell Scripting
- Script debloater (`debloat.py`) hanya boleh menargetkan aplikasi UWP pre-installed bawaan yang aman dihapus (jangan menghapus komponen krusial sistem seperti Windows Security atau Shell Experience).
- Gunakan `pwsh` atau `powershell` dengan parameter aman seperti `-NoProfile -NonInteractive` ketika memanggil subprocess dari Python.

## 5. Standar Pengujian (Testing)
- Setiap kali menambahkan aplikasi baru, preset, tweak, atau fitur debloat, **wajib** menjalankan `python test_installer.py` dan memastikan seluruh pengujian lolos tanpa error.
