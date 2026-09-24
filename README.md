# Projek Kriptografi 1

Tugas mata kuliah **Kriptografi — Semester 5**.

Repositori dipakai bareng anggota kelompok (**Windows**).
**Setup sekali → edit di VS Code → Ctrl+S → otomatis ke-push & ke-pull dari GitHub.**

| | |
|---|---|
| Repo | https://github.com/Abhiprayaa29/projek-kriptografi-1 |
| Branch utama | `main` |
| OS anggota | Windows |

> **Catatan:** seluruh sistem auto-sync di repo ini (**hanya untuk koneksi / sinkronisasi**, bukan logika projek kriptografi). Toolkit ini generik: salin ke repo lain (tugas kuliah, projek bareng, dsg.), ganti URL repo + nama folder, langsung jalan. Lihat **Pakai di projek lain** di bawah.

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
| Teman push/folder baru di GitHub | Ikut ke-pull (~2 detik) |

**Selesai.** Tidak perlu buka PowerShell lagi untuk kerja harian.

> **Sudah join SEBELUM fitur pull otomatis?**  
> Jalankan **sekali** (atau jalankan ulang baris `join.ps1` di atas — sekarang ikut `git pull`):
> ```powershell
> cd "$env:USERPROFILE\Documents\Kuliah\semester-5\kriptografi"
> git pull
> ```
> Atau hapus folder itu, jalankan ulang 1 baris `join.ps1` (clone fresh).

### Cek sync jalan

**Cek cepat (semua status dalam 1 layar):**

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\cek-sync.ps1
```

Atau buka file `.autosync.log` di folder repo. Kalau ada baris:

```
2026-09-24 18:05:12 PUSHED: M README.md;
2026-09-24 18:05:15 PULLED: update dari GitHub
2026-09-24 18:05:20 PUSHED: push 1 commit lokal (tree bersih)
```

berarti aman (push = perubahanmu ter-upload; pull = update teman ter-download).

- `PUSHED: M ...` / `COMMIT_OK_PUSH_FAIL` = ada file lokal di-commit lalu push (gagal = lihat baris FAIL).
- `PUSHED: push N commit lokal (tree bersih)` = commit lokal yang belum ada di GitHub berhasil ke-push (tree sudah bersih, tidak ada file baru lagi).
- `PUSH FAIL ... timeout after 45s` = `git push/pull` sempat hang (misal nunggu login) → di-kill otomatis, watcher tetap jalan dan coba lagi. Kalau ini muncul terus-menerus: login GitHub sekali di jendela interaktif (lihat troubleshooting).

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
| Folder/file teman gak muncul | Tunggu ~2 detik; kalau masih hilang, `git pull` sekali (lihat catatan “sudah join”) |
| Mau jeda sync sementara | `Stop-ScheduledTask -TaskName autosync-projek-kriptografi` |
| Konflik (teman edit file sama) | Lihat **Aturan kolaborasi** di bawah |
| File teman **tidak masuk** ke PC-mu | Tunggu ~2 detik. Masih hilang → jalankan sekali `git pull` di folder repo. Masih hilang → **file teman belum ke-push** (bukan salah pull-mu) — minta teman jalankan `cek-sync.ps1` |
| File-ku **tidak ke-push** ke GitHub | Lihat `.autosync.log` → baris `PUSH FAIL` / `COMMIT_OK_PUSH_FAIL`. Paling sering: **belum login GitHub**. Fix: buka PowerShell di folder repo → `git push` → login popup → centang remember. Lalu jalankan `powershell -ExecutionPolicy Bypass -File .\cek-sync.ps1` |
| Log bilang `timeout after 45s (proses git di-kill)` | Git sempat hang (biasanya nunggu popup login yang tidak muncul di jendela Hidden). Fix: buka PowerShell **interaktif** di folder repo → `git push` → login sekali → centang remember. Setelah itu restart task: `Stop-ScheduledTask -TaskName autosync-projek-kriptografi` lalu `Start-ScheduledTask ...`. |
| Sync macet total (log cuma `watcher started`) atau error parameter di log | **1 eksekusi:** `powershell -NoProfile -ExecutionPolicy Bypass -File .\fix-sync.ps1` (print progres `1/5`..`5/5`: pull fix + restart task + diagnosa). Kalau output tidak muncul, jalankan langsung di shell: `.\fix-sync.ps1`. Kalau masih sama, paste hasilnya ke chat. |

---

## Cara kerja auto-sync

```
auto-sync  ──polling tiap 2 detik──▶  ada perubahan lokal?
                                        │ ya                     │ tidak
                                        ▼                        ▼
                                 git add + commit          (lokal bersih)
                                        │                        │
                                        └──────────┬─────────────┘
                                                   ▼
                                    git pull --rebase + git push
                                                   │
                                    ┌──────────────┴──────────────┐
                                    ▼                             ▼
                             ada commit lokal            hanya remote yang baru
                                    │                             │
                                    ▼                             ▼
                                 PUSHED                    PULLED (update teman
                                                            muncul ~2 detik)
```

- **Dua arah:** push perubahanmu **dan** pull perubahan teman (folder/file baru muncul otomatis).
- Jalan otomatis **setiap login Windows** (Scheduled Task).
- Offline: commit lokal dulu, push/pull menyusul begitu online.
- Teman edit file yang sama: otomatis `pull --rebase` lalu push ulang.
- Nama di pesan commit = identitas git masing-masing (otomatis dari nama Windows).
- **Anti-hang:** tiap perintah git (`pull`/`push`) diberi timeout (Windows **45 detik**, Linux owner **30 detik**); kalau hang (misal nunggu login / network macet), proses di-kill → masuk log sebagai `FAIL ... timeout` → loop tetap jalan dan coba lagi siklus berikutnya. Watcher tidak pernah macet diam-diam.
- Setiap `push` yang sukses selalu tercatat di log (`PUSHED: ...`), termasuk saat tree sudah bersih tapi masih ada commit lokal yang belum ke GitHub.

---

## Struktur repo

```
projek-kriptografi-1/
├── Projek Kriptografi 1      # file tugas utama
├── README.md                 # file ini
├── join.ps1                  # ⚡ plug & play (1 baris PowerShell)
├── cek-sync.ps1              # diagnosa 1 tombol (auth, task, log, push)
├── fix-sync.ps1              # 1 eksekusi: progres 1/5..5/5 (pull + restart task + diagnosa)
├── GABUNG.bat                # klik dua kali (kalau folder sudah ada)
├── join-local.ps1            # launcher GABUNG.bat
├── auto-sync.ps1             # watcher auto-commit + pull + push (Windows; timeout 45s anti-hang)
├── setup-autosync.ps1        # ⚡ setup sekali: daftarkan Scheduled Task (1 script Windows)
├── setup-autosync.bat        # klik dua kali = setup
├── start-auto-sync.bat       # klik dua kali = sync sekali jalan
├── auto-sync.sh              # versi Linux (owner): commit + pull + push
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

### 3. Auto-sync — **1 script**

Dari folder repo, jalankan **sekali**:

```bat
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup-autosync.ps1
```

(Atau klik dua kali **`setup-autosync.bat`** — isinya perintah yang sama.)

Script itu: cek git + identitas → daftarkan Scheduled Task → start watcher → warmup auth GitHub (popup login mungkin muncul sekali).

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

## Untuk owner: sharing & setup

Bagian ini hanya untuk **pemilik repo** (Abhiprayaa29). Anggota kelompok tidak perlu langkah ini.

### 1. Invite anggota sebagai collaborator

Tanpa invite, `join.ps1` / `git clone` gagal (403). Dua cara, hasilnya sama.

**Via web (paling mudah, di browser mana pun):**

1. Buka https://github.com/Abhiprayaa29/projek-kriptografi-1/settings/access
2. Klik **Add people**
3. Ketik username / email GitHub teman → pilih permission **Write** → **Add**
4. Kirim link undangan ke teman; dia harus klik **Accept invitation**

**Via CLI (Linux owner, butuh `gh` sudah login):**

```bash
gh api -X PUT repos/Abhiprayaa29/projek-kriptografi-1/collaborators/<USERNAME_GITHUB> -f permission=push
```

Ganti `<USERNAME_GITHUB>` dengan username GitHub teman. Cek daftar yang sudah invite:

```bash
gh api repos/Abhiprayaa29/projek-kriptografi-1/collaborators --jq '.[].login'
```

### 2. Share link setup ke anggota

Kirim **1 baris ini** ke teman (Windows):

```text
irm https://raw.githubusercontent.com/Abhiprayaa29/projek-kriptografi-1/main/join.ps1 | iex
```

Atau arahkan dia ke bagian **Cara pakai (anggota kelompok)** di README ini.

### 3. Auto-sync owner: Windows

Kalau owner juga pakai Windows (bukan Linux):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup-autosync.ps1
```

Atau klik dua kali **`setup-autosync.bat`**. Task Scheduler: `autosync-projek-kriptografi`.

### 4. Auto-sync owner: Linux

```bash
bash setup-autosync.sh   # systemd user service
```

Stop/start: `systemctl --user stop|start autosync-projek-kriptografi`

Anti-hang di Linux: `timeout 30` pada `git pull` / `git push` (variabel `GIT_TIMEOUT_SEC` di `auto-sync.sh`).

Log owner: buka `.autosync.log` di folder repo (baris `PUSHED` / `PULLED` / `FAIL`).
