# Projek Kriptografi 1

Tugas mata kuliah **Kriptografi — Semester 5**.

Repositori ini dipakai bareng-bareng anggota kelompok (**semuanya Windows**).
Setelah setup sekali, tinggal **simpan file di VS Code (Ctrl+S)** — perubahan
otomatis di-commit dan di-push ke GitHub.

| | |
|---|---|
| Repo | https://github.com/Abhiprayaa29/projek-kriptografi-1 |
| Branch utama | `main` |
| OS anggota | Windows |
| Auto-sync | `auto-sync.ps1` + Scheduled Task |

---

## ⚡ Plug & Play (yang ini aja, cukup)

Buka **PowerShell** (Start Menu → ketik `PowerShell`), **copy-paste satu baris ini**, Enter:

```powershell
irm https://raw.githubusercontent.com/Abhiprayaa29/projek-kriptografi-1/main/join.ps1 | iex
```

Script akan otomatis:

1. Install **Git** kalau belum ada (via winget)
2. Isi identitas commit **otomatis** (nama Windows / username GitHub) — tanpa tanya
3. Clone repo ke `Documents\Kuliah\semester-5\kriptografi`
4. Pasang **auto-sync** (jalan tiap login)
5. Buka **VS Code** di folder repo

**Nol input.** Habis jalan: **Ctrl+S** → otomatis push ke GitHub.

> **Syarat:** invite dulu sebagai collaborator  
> (owner: repo → Settings → Collaborators → Add people).  
> Tanpa invite, clone/push akan gagal (403).

**Alternatif kalau sudah punya folder repo** ( hasil clone manual / ZIP ):  
klik dua kali **`GABUNG.bat`** di dalam folder itu.

---

## Setup manual (Windows, langkah demi langkah)

### Prasyarat

- **Git for Windows** — https://git-scm.com/download/win
  (saat install, pilih *Git Bash Here* / default saja)
- **VS Code** — https://code.visualstudio.com
- Akun GitHub + akses push ke repo ini  
  (minta owner invite: repo → **Settings** → **Collaborators** → **Add people**)

### Langkah 1 — clone repo

Buka **Git Bash** (klik kanan di folder mana pun → *Git Bash Here*), atau
**PowerShell** / **CMD**:

```bat
git clone https://github.com/Abhiprayaa29/projek-kriptografi-1.git
cd projek-kriptografi-1
```

> Lokasi bebas. Contoh enak di `D:\Kuliah\semester-5\kriptografi`  
> (clone dulu di mana saja, lalu pindahkan folder-nya kalau mau).

### Langkah 2 — identitas git (sekali saja)

Di terminal yang sama:

```bat
git config --global user.name  "Nama Kamu"
git config --global user.email "email-kamu@contoh.com"
```

`user.name` dipakai di pesan commit — jadi di GitHub kelihatan siapa yang
mengubah apa.

### Langkah 3 — setup auto-sync (sekali saja)

**Cara termudah:** buka folder hasil clone di File Explorer,  
**klik dua kali `setup-autosync.bat`**.

Atau dari terminal di dalam folder repo:

```bat
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup-autosync.ps1
```

Script ini akan:

1. Cek `git` + identitas git
2. Mendaftarkan **Scheduled Task** `autosync-projek-kriptografi`
   (jalan otomatis setiap kamu login Windows)
3. Menjalankan auto-sync sekarang juga

### Langkah 4 — buka di VS Code

```bat
code .
```

Selesai. Dari sekarang:

- **Ubah file → Ctrl+S** → otomatis ke-push (~3 detik)
- **Tambah file baru** → otomatis ke-add, ke-commit, ke-push
- **Hapus file** → ikut ter-sync juga

### Cek apakah jalan

PowerShell:

```powershell
Get-ScheduledTask -TaskName autosync-projek-kriptografi | Format-Table TaskName, State
Get-Content .autosync.log -Tail 20
```

Contoh baris log yang berhasil:

```
2026-09-24 17:34:01 PUSHED: M "Projek Kriptografi 1"; ?? tambahan.txt;
```

### Stop / start / hapus auto-sync

PowerShell (dari folder repo):

```powershell
Stop-ScheduledTask  -TaskName autosync-projek-kriptografi   # jeda
Start-ScheduledTask -TaskName autosync-projek-kriptografi   # lanjut
Unregister-ScheduledTask -TaskName autosync-projek-kriptografi -Confirm:$false  # hapus
```

Atau: **Task Scheduler** → *Task Scheduler Library* →
`autosync-projek-kriptografi` → Run / Disable / Delete.

### Auto-sync tanpa Scheduled Task (opsional)

Kalau tidak mau daftar Task Scheduler, setiap kali mau mulai sync:

1. Klik dua kali **`start-auto-sync.bat`**
2. Biarkan jendela PowerShell hitam itu terbuka
3. Tutup jendela = sync berhenti

---

## Setup manual (tanpa auto-sync)

Kalau tidak mau auto-sync, pakai Source Control bawaan VS Code:

1. Buka folder repo di VS Code
2. Panel **Source Control** (Ctrl+Shift+G)
3. File yang diubah / file baru otomatis muncul sebagai perubahan
4. Tulis pesan commit → **Commit** → **Push**

Atau via terminal (Git Bash / PowerShell):

```bat
git add -A
git commit -m "jenis perubahan: keterangan singkat"
git pull --rebase --autostash
git push
```

> Selalu `git pull --rebase --autostash` **sebelum** push, supaya tidak
> bentrok dengan commit teman.

---

## Cara kerja auto-sync

```
auto-sync.ps1  ──polling tiap 2 detik──▶  ada perubahan?
                                            │ ya
                                            ▼
                                     git add -A
                                            │
                                            ▼
                          git commit "auto-sync: <waktu> [<nama>]"
                                            │
                                            ▼
                                      git push  ──▶  GitHub
                                            │ gagal (mis. teman push duluan)
                                            ▼
                       git pull --rebase --autostash  →  push ulang
```

- Mutex mencegah dua instance auto-sync jalan bareng.
- Kalau offline: commit tetap tersimpan lokal, push menyusul otomatis
  saat ada koneksi dan watcher masih jalan.
- Kalau push ditolak karena teman push duluan: script otomatis
  `pull --rebase` lalu push ulang.
- Identitas commit memakai `git config user.name` masing-masing.

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
2. Kalau terjadi **konflik** saat pull:
   - Hentikan dulu auto-sync:
     `Stop-ScheduledTask -TaskName autosync-projek-kriptografi`
   - Selesaikan konflik di VS Code (Source Control menandai file konflik)
   - Lalu:
     ```bat
     git add .
     git rebase --continue
     git push
     ```
   - Nyalakan lagi: `Start-ScheduledTask -TaskName autosync-projek-kriptografi`
3. File rahasia (API key, `.env`) dan file besar jangan di-commit —
   tambahkan ke `.gitignore`.
4. Sebelum presentasi / deadline: pastikan bersih dan sudah ke-push semua:
   ```bat
   git status
   git log origin/main..HEAD
   ```
   `git status` kosong + `git log ...HEAD` kosong = aman.

---

## Linux (owner)

Anggota Windows pakai panduan di atas. Di Linux:

```bash
git config --global user.name  "Nama"
git config --global user.email "email@contoh.com"
bash setup-autosync.sh   # systemd user service
```

Stop/start: `systemctl --user stop|start autosync-projek-kriptografi`
