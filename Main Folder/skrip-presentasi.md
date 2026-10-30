# Skrip Presentasi: Aplikasi Kriptografi (gabungan.py)

Durasi target: 10 sampai 12 menit. Format: demo langsung di browser sambil bicara.
Semua nilai di bawah ini sudah diuji dan cocok dengan output aplikasi yang sebenarnya.

---

## 0. Persiapan (5 menit sebelum tampil)

1. Buka terminal di folder proyek, jalankan:

   ```
   streamlit run gabungan.py
   ```

2. Buka http://localhost:8501 di browser. Perbesar tampilan (Ctrl +) supaya tabel terbaca dari belakang.
3. Siapkan urutan tab: buka satu tab browser untuk aplikasi, satu tab untuk slide (kalau ada).
4. Isi dulu semua kolom di bawah ini sekali sebagai latihan, lalu refresh halaman agar bersih.

Sampel demo yang dipakai:

| Metode | Input | Kunci | Output |
|---|---|---|---|
| Caesar | Halo Dunia | 3 | Kdor Gxqld |
| Caesar brute force | Kdor Gxqld | semua 1-25 | baris kunci 3 = Halo Dunia |
| Vigenere | Halo Dunia | KUNCI | Ruyq Lehvc |
| XOR | Halo | SECRET | hex: 1b242f3d |
| RSA | Halo | Preset 1 (p=17, q=19, e=5) | 21 241 109 42 |
| Super | Tes Super | shift 3, KUNCI, SECRET, Preset 1 | 39 286 264 190 3 84 250 286 161 |

---

## 1. Pembukaan (0:00 - 1:00)

Yang dilakukan: aplikasi sudah terbuka di metode Caesar Cipher.

Yang dikatakan:

> "Aplikasi ini adalah implementasi lima metode kriptografi dalam satu antarmuka berbasis Streamlit.
> Lima metodenya: Caesar Cipher, Vigenere Cipher, XOR Cipher, RSA Cipher, dan Super Enkripsi yang
> menggabungkan keempatnya.
>
> Semua metode dipilih dari sidebar kiri. Setiap metode punya dua kemampuan yang sama: enkripsi dan
> dekripsi, ditambah tampilan proses per karakter atau per byte supaya langkah perhitungannya bisa
> ditelusuri, bukan hanya hasil akhirnya.
>
> Saya akan mendemokan empat metode satu per satu, lalu menutup dengan Super Enkripsi sebagai
> gabungan keempatnya."

Poin yang ditekankan: satu aplikasi, lima metode, setiap proses bisa dilihat detailnya.

---

## 2. Caesar Cipher (1:00 - 2:30)

Yang dilakukan:
1. Sidebar: pilih `Caesar Cipher`.
2. Tab `Enkripsi`: isi plaintext `Halo Dunia`, kunci pergeseran `3`.
3. Klik `Proses Enkripsi`.
4. Buka expander `Lihat detail proses per karakter`.
5. Pindah ke tab `Brute Force`, isi `Kdor Gxqld`, klik `Jalankan Brute Force`.
6. Scroll tabel brute force sampai baris kunci 3.

Yang dikatakan:

> "Caesar Cipher adalah substitusi geser. Setiap huruf digeser sejauh nilai kunci, rumusnya
> C sama dengan M ditambah shift, modulo 26 untuk enkripsi. Saya masukkan 'Halo Dunia' dengan
> geseran 3, hasilnya 'Kdor Gxqld': H jadi K, a jadi d, dan seterusnya. Spasi tidak berubah.
>
> Detail per karakter menampilkan posisi awal, besar geseran, posisi hasil, dan karakter hasilnya,
> jadi perhitungannya bisa dicek manual baris per baris.
>
> Kelemahan Caesar adalah ruang kuncinya hanya 25 kemungkinan. Itu sebabnya ada tab brute force:
> saya masukkan ciphertext tanpa tahu kuncinya, aplikasi mencoba semua kunci 1 sampai 25 sekaligus.
> Pada baris kunci 3 hasilnya 'Halo Dunia', jadi kuncinya ketemu hanya dengan melihat mana yang
> bahasanya masuk akal."

Yang muncul: ciphertext `Kdor Gxqld`, tabel detail dengan kolom No, Karakter, Posisi Awal, Hasil Geser, Karakter Hasil, lalu tabel brute force 25 baris (kolom Kunci, Hasil).

---

## 3. Vigenere Cipher (2:30 - 4:00)

Yang dilakukan:
1. Sidebar: pilih `Vigenere Cipher`.
2. Mode `Enkripsi`, plaintext `Halo Dunia`, kunci `KUNCI`.
3. Klik `Proses`.
4. Lihat subheader `Tampilan Proses Enkripsi` dan tabel di expander `Lihat detail proses per karakter`.
5. (opsional) ganti mode ke `Dekripsi`, tempel `Ruyq Lehvc`, kunci `KUNCI`, klik `Proses`.

Yang dikatakan:

> "Vigenere memperbaiki kelemahan Caesar. Kuncinya berupa kata, bukan satu angka, dan huruf kunci
> dipakai bergantian secara siklis. 'Halo Dunia' dengan kunci 'KUNCI' menghasilkan 'Ruyq Lehvc'.
>
> Perhatikan tabelnya: setiap huruf punya geseran yang berbeda karena huruf kuncinya berbeda.
> H dapat K berarti geser 10, a dapat U berarti geser 20, l dapat N berarti geser 13, o dapat C
> berarti geser 2, lalu kunci berulang lagi untuk kata kedua. Spasi dan tanda baca tidak diubah dan
> tidak memakai posisi kunci.
>
> Efeknya, pola frekuensi huruf pada teks asli jadi tersamar, sehingga analisis frekuensi sederhana
> tidak cukup. Vigenere baru bisa dipecah kalau panjang teksnya cukup panjang untuk analisis Kasiski,
> yaitu menebak panjang kunci dari jarak pengulangan pola."

Yang muncul: ciphertext `Ruyq Lehvc`, tabel 10 baris dengan kolom No, Karakter, Kunci, Posisi Awal, Geseran, Posisi Hasil, Karakter Hasil.

---

## 4. XOR Cipher (4:00 - 5:30)

Yang dilakukan:
1. Sidebar: pilih `XOR Cipher`.
2. Mode `Enkripsi`, format input `Teks`, data `Halo`, key `SECRET`.
3. Klik `Proses`.
4. Tunjukkan tabel proses, lalu tiga kotak hasil: Huruf (Teks), Biner, Heksadesimal.
5. (opsional) ganti mode ke `Dekripsi`, data `1b242f3d`, format `Heksadesimal`, key `SECRET`.

Yang dikatakan:

> "XOR bekerja di level bit, bukan huruf. Tiap byte data di-XOR dengan byte kunci, dan kalau kunci
> lebih pendek, kunci diulang. Rumusnya sederhana: plaintext XOR key sama dengan ciphertext, dan
> ciphertext XOR key yang sama menghasilkan plaintext lagi, karena a XOR b XOR b sama dengan a.
> Sifat inilah yang membuat XOR disebut simetris: satu kunci untuk dua arah.
>
> Saya masukkan 'Halo' dengan kunci 'SECRET'. Hasilnya di level byte: H bernilai 72 di-XOR dengan S
> bernilai 83 menghasilkan 27, dan seterusnya. Total hasilnya dalam heksadesimal 1b242f3d.
>
> Hasil XOR berupa byte apa saja, jadi sering tidak bisa dibaca sebagai teks. Karena itu aplikasi
> menampilkan tiga bentuk sekaligus: teks, biner, dan heksadesimal. Bentuk biner dan heksadesimal
> dipakai saat menyalin ciphertext supaya karakter kontrol tidak hilang."

Yang muncul: tabel 4 baris (No, Huruf, ASCII, Biner, Key, ASCII Key, Biner Key, XOR biner, Hasil dec, Hasil hex, Hasil karakter), tiga kotak hasil: `\x1b$/=`, `00011011 00100100 00101111 00111101`, `1b242f3d`.

---

## 5. RSA Cipher (5:30 - 7:30)

Yang dilakukan:
1. Sidebar: pilih `RSA Cipher`.
2. Bagian 1 (Kunci): mode kunci `Preset Otomatis`, preset `Preset 1 (p=17, q=19)`.
3. Tunjukkan baris hasil kunci: n = 323, phi(n) = 288, d = 173, plus kotak Public Key dan Private Key.
4. Tab `Enkripsi`: plaintext `Halo`, klik `Enkripsi`.
5. Salin angka hasil enkripsi, pindah ke tab `Dekripsi`, tempel, klik `Dekripsi`.
6. (opsional) ganti mode kunci ke `Manual (p, q, e)`, isi p = 4 untuk memperlihatkan pesan error validasi.

Yang dikatakan:

> "RSA berbeda dari tiga metode sebelumnya: ini kriptografi asimetris, kuncinya sepasang.
> Kunci publik (e, n) untuk enkripsi, kunci privat (d, n) untuk dekripsi.
>
> Alurnya: pilih dua bilangan prima p dan q, hitung n sama dengan p kali q, hitung phi(n) sama dengan
> (p-1)(q-1), pilih e yang koprima dengan phi(n), lalu hitung d sebagai invers modular e terhadap
> phi(n). Dengan p = 17 dan q = 19 didapat n = 323, phi(n) = 288, e = 5, dan d = 173.
>
> Enkripsi memakai C sama dengan M pangkat e mod n. Huruf H punya kode ASCII 72, sehingga
> 72 pangkat 5 mod 323 menghasilkan 21. 'Halo' jadi 21 241 109 42. Dekripsi memakai M sama dengan
> C pangkat d mod n, dan hasilnya kembali 'Halo'.
>
> Satu hal penting: nilai ASCII tiap karakter harus lebih kecil dari n, kalau tidak hasilnya ambigu.
> Karena byte ASCII sampai 255, n harus di atas 255. Itu sebabnya preset di aplikasi memakai
> n = 323, 299, dan 437. Kalau p dan q terlalu kecil, aplikasi menolak dan menampilkan pesan error."

Yang muncul: `n = 17 x 19 = 323 | phi(n) = 288 | d = 173`, Public Key (5, 323), Private Key (173, 323), ciphertext `21 241 109 42`, tabel proses dengan kolom No, Karakter, M (ASCII), Perhitungan (mis. `72^5 mod 323`), C; dekripsi menghasilkan `Halo`.

---

## 6. Super Enkripsi (7:30 - 10:00) - bagian utama

Yang dilakukan:
1. Sidebar: pilih `Super Enkripsi`.
2. Tunjukkan bagian `Pengaturan Kunci`: expander Caesar/Vigenere/XOR (default shift 3, KUNCI, SECRET) dan expander RSA (Preset 1, n = 323).
3. Tab `Mode Enkripsi`: plaintext `Tes Super`, klik `Enkripsi Sekarang`.
4. Tunjukkan `Ciphertext Final`, lalu scroll melalui empat expander tahap: Caesar, Vigenere, XOR, RSA.
5. Salin ciphertext, pindah ke tab `Mode Dekripsi`, tempel, klik `Dekripsi Sekarang`.
6. Scroll empat expander tahap dekripsi, tunjukkan hasil akhir `Tes Super`.

Yang dikatakan:

> "Super Enkripsi adalah inti aplikasi ini: empat algoritma dirangkai berurutan dalam satu proses.
> Enkripsi berjalan Plaintext ke Caesar, ke Vigenere, ke XOR, ke RSA, keluar sebagai daftar angka.
> Dekripsi berjalan terbalik: RSA, XOR, Vigenere, Caesar.
>
> Saya masukkan 'Tes Super'. Tahap 1 Caesar dengan geseran 3 menghasilkan 'Whv Vxshu'. Hasil itu
> masuk ke tahap 2, Vigenere dengan kunci 'KUNCI', menjadi 'Gbi Xfcbh'. Tahap 2 masuk ke tahap 3,
> diubah ke byte UTF-8 lalu di-XOR dengan kunci 'SECRET'. Tahap 4, tiap byte dienkripsi RSA dengan
> e = 5 dan n = 323, sehingga ciphertext akhirnya 39 286 264 190 3 84 250 286 161.
>
> Setiap tahap menampilkan tiga hal: masukan tahap tersebut, hasilnya, dan tabel detail per karakter
> atau per byte, termasuk rumus yang dipakai. Jadi kalau ditanya 'kenapa hasilnya begini', semua
> langkahnya bisa dibuka satu per satu. Tahap 3 menunjukkan pasangan byte masukan dan byte kunci,
> tahap 4 menunjukkan M pangkat e mod n untuk setiap byte.
>
> Untuk dekripsi, saya tempel ciphertext tadi. Urutannya dibalik, dan hasil akhirnya kembali
> 'Tes Super'. Kunci yang dipakai sama di kedua arah: shift Caesar, kunci Vigenere, kunci XOR, dan
> pasangan RSA, hanya saja enkripsi memakai e sedangkan dekripsi memakai d."

Yang muncul: ciphertext `39 286 264 190 3 84 250 286 161`, rangkaian tahap `Tes Super` -> `Whv Vxshu` -> `Gbi Xfcbh` -> byte XOR -> angka RSA, empat tabel 9 baris, dan hasil dekripsi `Tes Super`.

---

## 7. Penutup (10:00 - 10:45)

Yang dikatakan:

> "Kesimpulannya, aplikasi ini menyatukan lima metode kriptografi dalam satu antarmuka: tiga metode
> klasik berbasis substitusi dan bit, satu metode asimetris, dan satu mode gabungan yang merangkai
> keempatnya.
>
> Nilai utama yang saya tonjolkan ada di transparansi proses. Setiap metode menampilkan tabel
> perhitungan per karakter atau per byte, sehingga hasilnya bisa diverifikasi manual, bukan hanya
> dipercaya dari output.
>
> Aplikasi ini dibuat untuk pembelajaran, jadi ada beberapa batasan yang saya sadari: RSA di sini
> memakai kunci kecil tanpa padding, dan panjang kunci Caesar serta XOR sengaja dibuat sederhana
> supaya mudah didemokan. Untuk keamanan produksi, standarnya adalah algoritma modern seperti AES
> dan RSA-OAEP dengan padding. Terima kasih."

---

## 8. Antisipasi pertanyaan

**Kenapa Caesar cepat dipecahkan?**
Ruang kuncinya hanya 25. Brute force 25 percobaan sudah cukup, dan analisis frekuensi juga bekerja karena satu huruf selalu bergeser dengan jumlah yang sama.

**Apa bedanya Vigenere dengan Caesar?**
Caesar memakai satu geseran untuk semua huruf. Vigenere memakai geseran berbeda per posisi sesuai huruf kunci yang berulang, sehingga pola frekuensi huruf tersamar.

**Kenapa XOR disebut simetris dan bisa dibalik?**
Karena operasi XOR bersifat involusi: a XOR b XOR b sama dengan a. Kunci yang sama dipakai untuk enkripsi dan dekripsi.

**Kenapa hasil XOR tidak terbaca?**
Karena hasilnya byte apa saja, termasuk karakter kontrol. Aplikasi menampilkan bentuk biner dan heksadesimal supaya ciphertext bisa disalin tanpa rusak.

**Kenapa RSA butuh dua kunci?**
Karena sifat asimetris: enkripsi memakai (e, n) yang boleh diketahui publik, sedangkan dekripsi memerlukan (d, n) yang dirahasiakan.

**Kenapa n harus lebih besar dari 255?**
Karena tiap karakter dienkripsi sebagai nilai ASCII 0 sampai 255, dan nilai pesan harus lebih kecil dari n agar hasil mod tidak ambigu.

**Kenapa d dihitung sebagai invers modular?**
Karena syaratnya e kali d kongruen 1 mod phi(n), sehingga (M pangkat e) pangkat d kembali menjadi M.

**Kenapa Super Enkripsi memakai empat lapis?**
Untuk menunjukkan bahwa beberapa lapis bisa dirangkai: substitusi (Caesar), polialfabetik (Vigenere), level bit (XOR), dan asimetris (RSA). Untuk keamanan nyata tetap dipakai algoritma standar dengan padding.

**Apakah aplikasi ini aman untuk produksi?**
Tidak. Ini alat pembelajaran: kunci RSA kecil, tanpa padding, dan kunci simetris pendek.

**Kenapa memakai Streamlit?**
Karena seluruh logika ditulis dalam Python murni dan antarmuka interaktif terbentuk tanpa perlu menulis frontend terpisah, sehingga waktu pengerjaan fokus ke algoritma.

**Kenapa setiap metode menampilkan tabel proses?**
Untuk verifikasi dan pembelajaran: dosen atau penguji bisa mengecek perhitungan per karakter atau per byte, dan error logika jadi mudah ditemukan.

---

## 9. Jika ada masalah saat demo

- Pesan "n harus lebih besar dari 255" di RSA: ganti ke preset lain atau perbesar p dan q. Ini perilaku benar, bukan bug, dan bisa dijadikan bahan penjelasan.
- Hasil XOR tampak aneh: tunjukkan kotak Biner dan Heksadesimal, bukan kotak Teks.
- Field kosong memunculkan peringatan kuning atau merah: memang validasi, jelaskan sebagai fitur.
- Tabel lebar: perkecil zoom browser atau scroll horizontal, tabel memakai lebar penuh.

---

## 10. Checklist 30 detik sebelum mulai

- [ ] Server jalan, http://localhost:8501 terbuka dan halaman termuat.
- [ ] Sidebar menampilkan lima metode.
- [ ] Sampel demo di bagian 0 sudah dihafal atau dibuka di catatan.
- [ ] Tab browser bersih (belum ada hasil lama) atau siap di-refresh.
- [ ] Ukuran font browser cukup besar untuk dibaca dari belakang.
