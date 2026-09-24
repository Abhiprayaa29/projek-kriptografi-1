# Projek Kriptografi 1

Tugas mata kuliah **Kriptografi — Semester 5**.

Repositori dipakai bareng anggota kelompok (**Windows**).
**Setup sekali → edit di VS Code → Ctrl+S → otomatis ke-push ke GitHub.**

| | |
|---|---|
| Repo | https://github.com/Abhiprayaa29/projek-kriptografi-1 |
| Branch utama | `main` |
| OS anggota | Windows |

---

## ⚡ Cara pakai (anggota kelompok)

### 1. Setup — paste 1 baris

Buka **PowerShell** (Start Menu → ketik `PowerShell` → Enter),  
**copy-paste** ini, lalu Enter:

```powershell
irm https://raw.githubusercontent.com/Abhiprayaa29/projek-kriptografi-1/main/join.ps1 | iex
```

**Jangan ketik apa-apa.** Biarkan jalan sampai tulisan `SELESAI`  
(lalu Enter sekali untuk tutup jendela).

Yang dilakukan script (semua otomatis):

1. Install **Git** kalau belum ada
2. Isi identitas commit otomatis (nama Windows — tanpa tanya)
3. Clone repo ke `Documents\Kuliah\semester-5\kriptografi`
4. Pasang **auto-sync** (jalan tiap login Windows)
5. Buka **VS Code** di folder repo

### 2. Login GitHub — sekali saja

Push pertama mungkin muncul **popup login GitHub** (browser / Git Credential Manager).

→ **Login pakai akun GitHub masing-masing**, centang biar diingat.

Setelah itu **tidak akan ditanya lagi**.

### 3. Kerja — cukup Ctrl+S

Di VS Code:

| Aksi | Hasil |
|---|---|
| Edit file → **Ctrl+S** | Otomatis ke-push (~3 detik) |
| File baru → simpan | Ikut ke-push |
| Hapus file | Ikut ter-sync |

**Selesai.** Tidak perlu buka PowerShell lagi untuk kerja harian.

### Cek sync jalan

Buka file `.autosync.log` di folder repo. Kalau ada baris:

```
2026-09-24 18:05:12 PUSHED: M README.md;
```

berarti aman.

> **Syarat sebelum step 1:** owner harus invite dulu sebagai collaborator.  
> Tanpa invite, clone/push gagal (403).

**Sudah punya folder repo** (clone manual / ZIP): klik dua kali **`GABUNG.bat`** di folder itu.

---

## Kalau ada masalah

| Masalah | Solusi |
|---|---|
| Popup login GitHub muncul | Login sekali, centang *remember* |
| Tidak ada popup / push gagal auth | Jalankan `gh auth login` di PowerShell (install [GitHub CLI](https://cli.github.com) dulu) |
| VS Code belum kebuka | Install dari https://code.visualstudio.com, lalu `code "%USERPROFILE%\Documents\Kuliah\semester-5\kriptografi"` |
| Mau lihat apakah sync jalan | Buka `.autosync.log` di folder repo |
| Mau jeda sync sementara | `Stop-ScheduledTask -TaskName autosync-projek-kriptografi` |
| Konflik (teman edit file sama) | Lihat **Aturan kolaborasi** di bawah |

---

## Cara kerja auto-sync

```
auto-sync  ──polling tiap 2 detik──▶  ada perubahan lokal?
                                        │ ya                    │ tidak (lokal bersih)
                                        ▼                       ▼
                                 git add -A              git pull (ambil update teman)
                                        │
                                        ▼
                          git commit + pull + push ──▶ GitHub
```

- **Dua arah:** push perubahanmu **dan** pull perubahan teman (folder/file baru muncul otomatis ~2 detik).
- Jalan otomatis **setiap login Windows** (Scheduled Task).
- Offline: commit lokal dulu, push/pull menyusul begitu online.
- Teman edit file yang sama: otomatis `pull --rebase` lalu push ulang.
- Nama di pesan commit = identitas git masing-masing (otomatis dari nama Windows).

---

## Struktur repo

```
projek-kriptografi-1/
├── Projek Kriptografi 1      # file tugas utama
├── README.md                 # file ini
├── join.ps1                  # ⚡ plug & play (1 baris PowerShell)
├── GABUNG.bat                # klik dua kali (kalau folder sudah ada)
├── join-local.ps1            # launcher GABUNG.bat
├── auto-sync.ps1             # watcher auto-commit + push (Windows)
├── setup-autosync.ps1        # setup Scheduled Task
├── setup-autosync.bat        # klik dua kali = setup
├── start-auto-sync.bat       # klik dua kali = sync sekali jalan
├── auto-sync.sh              # versi Linux (owner)
├── setup-autosync.sh         # versi Linux (owner)
├── .gitignore
└── .autosync.log             # log (tidak di-commit)
```

---

## Aturan kolaborasi

1. **Jangan force-push** — merusak commit anggota lain.
2. **Konflik** saat sync:
   - Jeda dulu: `Stop-ScheduledTask -TaskName autosync-projek-kriptografi`
   - Selesaikan konflik di VS Code (Source Control)
   - Lalu:
     ```bat
     git add .
     git rebase --continue
     git push
     ```
   - Nyalakan lagi: `Start-ScheduledTask -TaskName autosync-projek-kriptografi`
3. File rahasia (API key, `.env`) dan file besar jangan di-commit.
4. Sebelum deadline — pastikan sudah bersih di GitHub:
   ```bat
   git status
   git log origin/main..HEAD
   ```
   Dua-duanya kosong = aman.

---

## Setup manual (hanya kalau plug & play gagal)

### Prasyarat

- **Git for Windows** — https://git-scm.com/download/win
- **VS Code** — https://code.visualstudio.com
- Akun GitHub + sudah di-invite sebagai collaborator

### 1. Clone

```bat
git clone https://github.com/Abhiprayaa29/projek-kriptografi-1.git
cd projek-kriptografi-1
```

### 2. Identitas git (sekali saja — script plug & play juga mengisi ini otomatis)

```bat
git config --global user.name  "Nama Kamu"
git config --global user.email "email-kamu@contoh.com"
```

### 3. Auto-sync

Klik dua kali **`setup-autosync.bat`** di folder repo, atau:

```bat
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup-autosync.ps1
```

### 4. Buka VS Code

```bat
code .
```

### Cek / stop / start

```powershell
Get-ScheduledTask -TaskName autosync-projek-kriptografi | Format-Table TaskName, State
Get-Content .autosync.log -Tail 20

Stop-ScheduledTask  -TaskName autosync-projek-kriptografi   # jeda
Start-ScheduledTask -TaskName autosync-projek-kriptografi   # lanjut
Unregister-ScheduledTask -TaskName autosync-projek-kriptografi -Confirm:$false  # hapus
```

### Auto-sync tanpa Scheduled Task (opsional)

1. Klik dua kali **`start-auto-sync.bat`**
2. Biarkan jendela PowerShell terbuka
3. Tutup jendela = sync berhenti

### Tanpa auto-sync (manual di VS Code)

1. Buka folder repo di VS Code
2. **Source Control** (Ctrl+Shift+G)
3. Tulis pesan commit → **Commit** → **Push**

Atau terminal:

```bat
git add -A
git commit -m "jenis perubahan: keterangan singkat"
git pull --rebase --autostash
git push
```

> Selalu `git pull --rebase --autostash` **sebelum** push.

---

## Linux (owner)

```bash
bash setup-autosync.sh   # systemd user service
```

Stop/start: `systemctl --user stop|start autosync-projek-kriptografi`
