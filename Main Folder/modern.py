"""
=======================================================================
 APLIKASI ENKRIPSI & DEKRIPSI
 Algoritma  : XOR Cipher & RSA
 Fitur      : Menampilkan langkah-langkah proses algoritma
=======================================================================
"""

import random
import math
import textwrap


# =======================================================================
# UTILITAS TAMPILAN
# =======================================================================

def garis(karakter="=", panjang=70):
    print(karakter * panjang)


def judul(teks):
    garis()
    print(teks.center(70))
    garis()


def sub_judul(teks):
    print("\n" + "-" * 70)
    print(f" {teks}")
    print("-" * 70)


def jeda():
    input("\nTekan ENTER untuk melanjutkan...")


# =======================================================================
# BAGIAN 1 : XOR CIPHER
# =======================================================================

def xor_proses(teks, key, mode):
    """
    Melakukan XOR antara setiap karakter teks dengan key (berulang),
    sekaligus menampilkan proses tiap karakter.
    """
    hasil = []
    key_len = len(key)

    sub_judul(f"PROSES {mode.upper()} - XOR CIPHER")
    print(f"{'No':<4}{'Karakter':<10}{'ASCII':<8}{'Key':<8}"
          f"{'ASCII Key':<12}{'XOR (dec)':<12}{'Hasil':<10}")
    garis("-")

    for i, ch in enumerate(teks):
        k = key[i % key_len]
        nilai_ascii = ord(ch)
        nilai_key = ord(k)
        nilai_xor = nilai_ascii ^ nilai_key
        hasil_char = chr(nilai_xor)
        hasil.append(hasil_char)

        # representasi aman untuk karakter non-printable saat ditampilkan
        tampil_char = ch if ch.isprintable() else repr(ch)
        tampil_hasil = hasil_char if hasil_char.isprintable() else repr(hasil_char)

        print(f"{i+1:<4}{tampil_char:<10}{nilai_ascii:<8}{k:<8}"
              f"{nilai_key:<12}{nilai_xor:<12}{tampil_hasil:<10}")

    return "".join(hasil)


def xor_encrypt(plaintext, key):
    hasil = xor_proses(plaintext, key, "ENKRIPSI")
    # tampilkan hasil enkripsi dalam bentuk hex agar aman dibaca / disalin
    hasil_hex = hasil.encode("utf-8", errors="surrogatepass").hex()
    return hasil, hasil_hex


def xor_decrypt(ciphertext_hex, key):
    try:
        bytes_data = bytes.fromhex(ciphertext_hex)
        ciphertext = bytes_data.decode("utf-8", errors="surrogatepass")
    except ValueError:
        print("\n[ERROR] Format ciphertext (hex) tidak valid!")
        return None
    hasil = xor_proses(ciphertext, key, "DEKRIPSI")
    return hasil


def menu_xor():
    while True:
        judul("MENU XOR CIPHER")
        print("1. Enkripsi")
        print("2. Dekripsi")
        print("3. Kembali ke Menu Utama")
        pilihan = input("\nPilih menu (1-3): ").strip()

        if pilihan == "1":
            sub_judul("INPUT ENKRIPSI XOR")
            plaintext = input("Masukkan plaintext (pesan asli): ")
            key = input("Masukkan key (kata kunci): ")
            if not key:
                print("[ERROR] Key tidak boleh kosong!")
                jeda()
                continue

            hasil, hasil_hex = xor_encrypt(plaintext, key)

            sub_judul("HASIL AKHIR")
            print(f"Plaintext   : {plaintext}")
            print(f"Key         : {key}")
            print(f"Ciphertext (hex) : {hasil_hex}")
            jeda()

        elif pilihan == "2":
            sub_judul("INPUT DEKRIPSI XOR")
            ciphertext_hex = input("Masukkan ciphertext (dalam format hex): ")
            key = input("Masukkan key (kata kunci): ")
            if not key:
                print("[ERROR] Key tidak boleh kosong!")
                jeda()
                continue

            hasil = xor_decrypt(ciphertext_hex, key)
            if hasil is not None:
                sub_judul("HASIL AKHIR")
                print(f"Ciphertext (hex) : {ciphertext_hex}")
                print(f"Key              : {key}")
                print(f"Plaintext        : {hasil}")
            jeda()

        elif pilihan == "3":
            break
        else:
            print("[ERROR] Pilihan tidak valid!")
            jeda()


# =======================================================================
# BAGIAN 2 : RSA
# =======================================================================

def is_prima(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def buat_bilangan_prima(bawah=100, atas=300):
    """Menghasilkan bilangan prima acak dalam rentang tertentu (untuk demo)."""
    kandidat = [n for n in range(bawah, atas) if is_prima(n)]
    return random.choice(kandidat)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def modinv(e, phi):
    """Mencari invers modular e terhadap phi menggunakan Extended Euclidean."""
    g, x, _ = extended_gcd(e, phi)
    if g != 1:
        raise Exception("Invers modular tidak ditemukan")
    return x % phi


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y


def rsa_buat_kunci():
    sub_judul("PEMBANGKITAN KUNCI RSA")

    p = buat_bilangan_prima()
    q = buat_bilangan_prima()
    while q == p:
        q = buat_bilangan_prima()

    n = p * q
    phi = (p - 1) * (q - 1)

    # pilih e yang coprime dengan phi
    e = 65537 if 65537 < phi and gcd(65537, phi) == 1 else 3
    while gcd(e, phi) != 1:
        e += 2

    d = modinv(e, phi)

    print(f"1. Pilih dua bilangan prima acak:")
    print(f"   p = {p}")
    print(f"   q = {q}")
    print(f"\n2. Hitung n = p * q")
    print(f"   n = {p} * {q} = {n}")
    print(f"\n3. Hitung phi(n) = (p-1) * (q-1)")
    print(f"   phi(n) = ({p}-1) * ({q}-1) = {phi}")
    print(f"\n4. Pilih e sehingga gcd(e, phi(n)) = 1")
    print(f"   e = {e}")
    print(f"\n5. Hitung d = e^(-1) mod phi(n)  (invers modular)")
    print(f"   d = {d}")
    print(f"\n>> Kunci Publik  (e, n) = ({e}, {n})")
    print(f">> Kunci Privat  (d, n) = ({d}, {n})")

    return {"p": p, "q": q, "n": n, "phi": phi, "e": e, "d": d}


def rsa_encrypt(teks, e, n):
    sub_judul("PROSES ENKRIPSI RSA")
    print("Rumus: C = M^e mod n\n")
    print(f"{'No':<4}{'Karakter':<10}{'M (ASCII)':<12}{'Perhitungan C = M^e mod n':<35}{'C':<10}")
    garis("-")

    hasil = []
    for i, ch in enumerate(teks):
        m = ord(ch)
        c = pow(m, e, n)
        hasil.append(c)
        perhitungan = f"{m}^{e} mod {n}"
        tampil_char = ch if ch.isprintable() else repr(ch)
        print(f"{i+1:<4}{tampil_char:<10}{m:<12}{perhitungan:<35}{c:<10}")

    return hasil


def rsa_decrypt(daftar_cipher, d, n):
    sub_judul("PROSES DEKRIPSI RSA")
    print("Rumus: M = C^d mod n\n")
    print(f"{'No':<4}{'C':<10}{'Perhitungan M = C^d mod n':<30}{'M (ASCII)':<12}{'Karakter':<10}")
    garis("-")

    hasil = []
    for i, c in enumerate(daftar_cipher):
        m = pow(c, d, n)
        try:
            karakter = chr(m)
        except ValueError:
            karakter = "?"
        hasil.append(karakter)
        perhitungan = f"{c}^{d} mod {n}"
        tampil_hasil = karakter if karakter.isprintable() else repr(karakter)
        print(f"{i+1:<4}{c:<10}{perhitungan:<30}{m:<12}{tampil_hasil:<10}")

    return "".join(hasil)


def menu_rsa():
    kunci = None
    while True:
        judul("MENU RSA")
        print("1. Generate Kunci (Public & Private)")
        print("2. Enkripsi")
        print("3. Dekripsi")
        print("4. Kembali ke Menu Utama")
        pilihan = input("\nPilih menu (1-4): ").strip()

        if pilihan == "1":
            kunci = rsa_buat_kunci()
            jeda()

        elif pilihan == "2":
            if kunci is None:
                print("\n[INFO] Kunci belum digenerate, sistem akan generate otomatis.")
                kunci = rsa_buat_kunci()
                jeda()

            plaintext = input("\nMasukkan plaintext (pesan asli): ")
            hasil = rsa_encrypt(plaintext, kunci["e"], kunci["n"])

            sub_judul("HASIL AKHIR")
            print(f"Plaintext  : {plaintext}")
            print(f"Kunci Publik (e, n) : ({kunci['e']}, {kunci['n']})")
            print(f"Ciphertext (list angka) : {hasil}")
            jeda()

        elif pilihan == "3":
            if kunci is None:
                print("\n[ERROR] Belum ada kunci. Silakan generate kunci terlebih dahulu (menu 1).")
                jeda()
                continue

            print("\nMasukkan ciphertext (angka dipisah spasi atau koma),")
            teks_cipher = input("contoh: 123 456 789 -> ")
            try:
                daftar_cipher = [int(x) for x in teks_cipher.replace(",", " ").split()]
            except ValueError:
                print("[ERROR] Format ciphertext tidak valid!")
                jeda()
                continue

            hasil = rsa_decrypt(daftar_cipher, kunci["d"], kunci["n"])

            sub_judul("HASIL AKHIR")
            print(f"Ciphertext : {daftar_cipher}")
            print(f"Kunci Privat (d, n) : ({kunci['d']}, {kunci['n']})")
            print(f"Plaintext  : {hasil}")
            jeda()

        elif pilihan == "4":
            break
        else:
            print("[ERROR] Pilihan tidak valid!")
            jeda()


# =======================================================================
# MENU UTAMA
# =======================================================================

def tampilkan_intro():
    judul("APLIKASI ENKRIPSI & DEKRIPSI")
    deskripsi = (
        "Aplikasi ini mendukung dua algoritma kriptografi modern, "
        "yaitu XOR Cipher (kriptografi simetris) dan RSA "
        "(kriptografi asimetris). Setiap proses enkripsi maupun "
        "dekripsi akan ditampilkan langkah demi langkah agar mudah dipahami."
    )
    for baris in textwrap.wrap(deskripsi, width=68):
        print(baris)
    garis()


def menu_utama():
    tampilkan_intro()
    while True:
        print("\nMENU UTAMA")
        print("1. XOR Cipher")
        print("2. RSA")
        print("3. Keluar")
        pilihan = input("\nPilih menu (1-3): ").strip()

        if pilihan == "1":
            menu_xor()
        elif pilihan == "2":
            menu_rsa()
        elif pilihan == "3":
            print("\nTerima kasih telah menggunakan aplikasi ini. Sampai jumpa!")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")
            jeda()


if __name__ == "__main__":
    menu_utama()