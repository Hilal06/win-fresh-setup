---
name: win-app-manager
description: Gunakan skill ini ketika user ingin menambah, mengubah, memvalidasi software di apps.json, atau memperbarui presets di win-fresh-setup.
---

# Win-App-Manager Skill

Skill ini memandu agen dalam mengelola katalog aplikasi Winget di `apps.json` dan profil preset di `presets.json`.

## Langkah-langkah Menambah Aplikasi Baru:

1. **Cari & Validasi Winget ID**:
   - Jika perlu mencari ID paket yang tepat, gunakan command:
     ```powershell
     winget search "<kata_kunci>" --exact
     ```
   - Pastikan ID yang didapat merupakan ID resmi dari vendor/publisher.

2. **Perbarui `apps.json`**:
   - Buka [apps.json](file:///D:/Workspace/Script/apps.json) dan sisipkan objek baru di kategori yang relevan:
     ```json
     {
       "category": "Kategori yang Sesuai",
       "name": "Nama Software",
       "id": "Vendor.PackageName",
       "description": "Fungsi singkat software",
       "default": false
     }
     ```

3. **(Opsional) Tambahkan ke Presets**:
   - Jika aplikasi cocok untuk preset tertentu (misal Developer atau Gamer), tambahkan ID-nya ke daftar `app_ids` di [presets.json](file:///D:/Workspace/Script/presets.json).

4. **Jalankan Verifikasi & Test Otomatis**:
   - Jalankan unit test validasi skema:
     ```powershell
     python test_installer.py
     ```
   - Pastikan Test 2 (`apps.json`) dan Test 3 (`presets.json`) berstatus `[OK]`.
