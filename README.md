# Projek Kriptografi 1

Tugas mata kuliah **Kriptografi — Semester 5**.

Repositori ini dipakai bareng-bareng anggota kelompok. Setiap anggota
yang sudah setup auto-sync tinggal **simpan file di VS Code**, perubahan
akan otomatis di-commit dan di-push ke GitHub.

| | |
|---|---|
| Repo | https://github.com/Abhiprayaa29/projek-kriptografi-1 |
| Branch utama | `main` |
| Auto-sync | `auto-sync.sh` + systemd user service |

---

## Setup untuk anggota kelompok (Linux)

### Prasyarat

- `git`
- Akun GitHub + akses push ke repo ini (minta owner invite sebagai collaborator:
  repo → **Settings** → **Collaborators** → **Add people**)
- VS Code
- systemd (biasanya sudah ada di Ubuntu/Debian/Fedora)

### Langkah 1 — clone repo

```bash
git clone https://github.com/Abhiprayaa29/projek-kriptografi-1.git
cd projek-kriptografi-1
```

> Lebih suka taruh di folder kuliah? Pindahkan saja hasil clone ke
> `~/kuliah/semester-5/kriptografi` (atau path favoritmu), lalu `cd` ke sana.
> Path bebas — script setup otomatis menyesuaikan.

### Langkah 2 — identitas git (sekali saja)

```bash
git config --global user.name  "Nama Kamu"
git config --global user.email "email-kamu@contoh.com"
```

### Langkah 3 — setup auto-sync (sekali saja)

```bash
bash setup-autosync.sh
```

Script ini akan:

1. Cek `git` + identitas git
2. Memberi izin execute pada `auto-sync.sh`
3. Memasang systemd user service
   (`~/.config/systemd/user/autosync-projek-kriptografi.service`)
4. Mengaktifkan service (jalan otomatis tiap login)

### Langkah 4 — buka di VS Code

```bash
code .
```

Selesai. Dari sekarang:

- **Ubah file → Ctrl+S** → otomatis ke-push (~3 detik)
- **Tambah file baru** → otomatis ke-add, ke-commit, ke-push
- **Hapus file** → ikut ter-sync juga

### Cek apakah jalan

```bash
# status service
systemctl --user status autosync-projek-kriptografi

# lihat log sync terakhir
tail -f .autosync.log
```

Contoh baris log yang berhasil:

```
2026-09-24 17:34:01 PUSHED: M "Projek Kriptografi 1"; ?? tambahan.txt;
```

---

## Setup manual (tanpa auto-sync)

Kalau tidak mau auto-sync, pakai Source Control bawaan VS Code:

1. Buka folder repo di VS Code
2. Panel **Source Control** (Ctrl+Shift+G)
3. File yang diubah / file baru otomatis muncul sebagai perubahan
4. Tulis pesan commit → **Commit** → **Push**

Atau via terminal:

```bash
git add -A
git commit -m "jenis perubahan: keterangan singkat"
git pull --rebase --autostash   # selalu tarik dulu sebelum push
git push
```

---

## macOS / Windows

`setup-autosync.sh` butuh systemd (Linux). Di macOS/Windows:

- **Cara termudah:** pakai **Source Control VS Code** (langkah manual di atas), atau
- **GitHub Desktop**, atau
- Jalankan watcher manual di Git Bash / WSL:

  ```bash
  bash auto-sync.sh
  ```

  (biarkan terminal itu terbuka selama mau auto-sync)

---

## Cara kerja auto-sync (anggota kelompok wajib tahu)

```
auto-sync.sh  ──polling tiap 2 detik──▶  ada perubahan?
                                            │ ya
                                            ▼
                                     git add -A
                                            │
                                            ▼
                              git commit "auto-sync: <waktu> [<nama>]"
                                            │
                                            ▼
                                      git push  ──▶  GitHub
                                            │ gagal (mis. sudah ada
                                            │ push dari teman)
                                            ▼
                              git pull --rebase --autostash  →  push ulang
```

- Lock file `.autosync.lock` mencegah dua proses sync bentrok.
- Kalau offline: commit tetap tersimpan lokal, push menyusul otomatis
  saat service jalan lagi dan ada koneksi.
- Kalau push ditolak karena teman push duluan: script otomatis
  `pull --rebase` lalu push ulang.
- Identitas commit memakai `git config user.name` masing-masing —
  jadi kelihatan siapa yang mengubah apa di riwayat commit.

### Stop / start / matikan

```bash
systemctl --user stop autosync-projek-kriptografi     # jeda
systemctl --user start autosync-projek-kriptografi    # lanjut
systemctl --user disable --now autosync-projek-kriptografi  # matikan total
```

---

## Struktur repo

```
projek-kriptografi-1/
├── Projek Kriptografi 1      # file tugas utama
├── README.md                 # file ini
├── auto-sync.sh              # watcher auto-commit + push
├── setup-autosync.sh         # setup sekali jalan untuk anggota
├── .gitignore
└── .autosync.log             # log (tidak di-commit)
```

---

## Aturan kolaborasi

1. **Jangan force-push** — merusak commit anggota lain.
2. Kalau terjadi konflik saat `pull --rebase`: selesaikan manual di VS Code
   (panel Source Control menandai file konflik), lalu
   ```bash
   git add .
   git rebase --continue
   git push
   ```
   Matikan dulu auto-sync selama menyelesaikan konflik:
   `systemctl --user stop autosync-projek-kriptografi`
   Setelah selesai: `systemctl --user start autosync-projek-kriptografi`
3. File besar / rahasia (API key, `.env`) jangan di-commit — tambahkan ke `.gitignore`.
4. Sebelum presentasi / deadline: pastikan `git status` bersih dan
   `git log origin/main..HEAD` kosong (artinya semua sudah ke-push).
