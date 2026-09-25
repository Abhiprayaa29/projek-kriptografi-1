"""
=======================================================================
 APLIKASI ENKRIPSI & DEKRIPSI
 Algoritma  : XOR Cipher & RSA
=======================================================================
"""

import math


# =======================================================================
# UTILITAS TAMPILAN
# =======================================================================

def garis():
    print("-" * 65)


def judul(teks):
    print("=" * 65)
    print(teks.center(65))
    print("=" * 65)


def jeda():
    input("\nTekan ENTER untuk melanjutkan...")


# =======================================================================
# BAGIAN 1 : XOR CIPHER
# =======================================================================

def xor_process(data, key, mode):
    """
    data : list of int (nilai byte 0-255)
    key  : string kunci
    Menampilkan tabel proses XOR dan mengembalikan list hasil (int).
    """
    key_bytes = [ord(k) for k in key]
    hasil = []

    print(f"\nProses {mode} (setiap byte di-XOR dengan key secara berulang):")
    print(f"{'No':<4}{'Input (dec)':<14}{'Key (dec)':<12}{'XOR (dec)':<12}")
    garis()

    for i, b in enumerate(data):
        k = key_bytes[i % len(key_bytes)]
        x = b ^ k
        hasil.append(x)
        print(f"{i+1:<4}{b:<14}{k:<12}{x:<12}")

    return hasil


def tampilkan_hex_biner(nilai_list):
    data_bytes = bytes(nilai_list)
    hasil_hex = data_bytes.hex()
    hasil_biner = " ".join(format(b, "08b") for b in data_bytes)
    return hasil_hex, hasil_biner


def menu_xor_encrypt():
    judul("XOR CIPHER - ENKRIPSI")
    plaintext = input("Masukkan plaintext: ")
    key = input("Masukkan key: ")
    if not key:
        print("[ERROR] Key tidak boleh kosong!")
        return

    data = [ord(c) for c in plaintext]
    hasil = xor_process(data, key, "ENKRIPSI")
    hasil_hex, hasil_biner = tampilkan_hex_biner(hasil)

    print("\nHASIL AKHIR")
    garis()
    print(f"Plaintext         : {plaintext}")
    print(f"Key               : {key}")
    print(f"Ciphertext (hex)  : {hasil_hex}")
    print(f"Ciphertext (biner): {hasil_biner}")


def menu_xor_decrypt():
    judul("XOR CIPHER - DEKRIPSI")
    print("Format ciphertext input:")
    print("1. Hexadecimal")
    print("2. Biner")
    format_pilih = input("Pilih format (1/2): ").strip()

    ciphertext = input("Masukkan ciphertext: ").strip().replace(" ", "")
    key = input("Masukkan key: ")
    if not key:
        print("[ERROR] Key tidak boleh kosong!")
        return

    try:
        if format_pilih == "1":
            data_bytes = bytes.fromhex(ciphertext)
        elif format_pilih == "2":
            if len(ciphertext) % 8 != 0:
                print("[ERROR] Panjang biner harus kelipatan 8!")
                return
            data_bytes = bytes(
                int(ciphertext[i:i + 8], 2) for i in range(0, len(ciphertext), 8)
            )
        else:
            print("[ERROR] Format pilihan tidak valid!")
            return
    except ValueError:
        print("[ERROR] Format ciphertext tidak valid!")
        return

    hasil = xor_process(list(data_bytes), key, "DEKRIPSI")
    plaintext = "".join(chr(x) for x in hasil)

    print("\nHASIL AKHIR")
    garis()
    print(f"Ciphertext : {ciphertext}")
    print(f"Key        : {key}")
    print(f"Plaintext  : {plaintext}")


def menu_xor():
    while True:
        judul("MENU XOR CIPHER")
        print("1. Enkripsi")
        print("2. Dekripsi")
        print("3. Kembali ke Menu Utama")
        pilihan = input("\nPilih menu (1-3): ").strip()

        if pilihan == "1":
            menu_xor_encrypt()
            jeda()
        elif pilihan == "2":
            menu_xor_decrypt()
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


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    return g, y1 - (b // a) * x1, x1


def modinv(e, phi):
    g, x, _ = extended_gcd(e, phi)
    if g != 1:
        raise ValueError("Invers modular tidak ditemukan")
    return x % phi


def input_prima(label):
    """Minta input bilangan prima dari user, ulangi jika tidak valid."""
    while True:
        teks = input(f"Masukkan {label} (bilangan prima): ").strip()
        if not teks.isdigit():
            print("[ERROR] Harus berupa angka!")
            continue
        n = int(teks)
        if not is_prima(n):
            print(f"[ERROR] {n} bukan bilangan prima! Silakan input ulang.")
            continue
        return n


def input_e(phi):
    """Minta input e dari user, harus 1 < e < phi dan gcd(e, phi) = 1."""
    while True:
        teks = input(f"Masukkan e (1 < e < {phi}, gcd(e, phi) = 1): ").strip()
        if not teks.isdigit():
            print("[ERROR] Harus berupa angka!")
            continue
        e = int(teks)
        if not (1 < e < phi):
            print(f"[ERROR] e harus di antara 1 dan {phi}!")
            continue
        if gcd(e, phi) != 1:
            print(f"[ERROR] e = {e} tidak coprime dengan phi(n) = {phi}. Pilih e lain!")
            continue
        return e


def rsa_buat_kunci():
    judul("PEMBANGKITAN KUNCI RSA")

    p = input_prima("p")
    while True:
        q = input_prima("q")
        if q == p:
            print("[ERROR] q tidak boleh sama dengan p!")
            continue
        break

    n = p * q
    phi = (p - 1) * (q - 1)

    print(f"\nn         = p * q             = {p} * {q} = {n}")
    print(f"phi(n)    = (p-1) * (q-1)     = {p-1} * {q-1} = {phi}")

    e = input_e(phi)
    d = modinv(e, phi)

    print(f"\nd (e^-1 mod phi(n)) = {d}")
    print(f"\n>> Kunci Publik  (e, n) = ({e}, {n})")
    print(f">> Kunci Privat  (d, n) = ({d}, {n})")

    return {"p": p, "q": q, "n": n, "phi": phi, "e": e, "d": d}


def rsa_encrypt(teks, e, n):
    print(f"\nRumus: C = M^e mod n")
    print(f"{'No':<4}{'Karakter':<10}{'M':<8}{'Perhitungan':<25}{'C':<10}")
    garis()

    hasil = []
    for i, ch in enumerate(teks):
        m = ord(ch)
        if m >= n:
            print(f"[ERROR] Karakter '{ch}' (ASCII {m}) >= n ({n}). "
                  f"Pilih p, q yang lebih besar!")
            return None
        c = pow(m, e, n)
        hasil.append(c)
        print(f"{i+1:<4}{ch:<10}{m:<8}{f'{m}^{e} mod {n}':<25}{c:<10}")

    return hasil


def rsa_decrypt(daftar_cipher, d, n):
    print(f"\nRumus: M = C^d mod n")
    print(f"{'No':<4}{'C':<10}{'Perhitungan':<22}{'M':<8}{'Karakter':<10}")
    garis()

    hasil = []
    for i, c in enumerate(daftar_cipher):
        m = pow(c, d, n)
        karakter = chr(m)
        hasil.append(karakter)
        print(f"{i+1:<4}{c:<10}{f'{c}^{d} mod {n}':<22}{m:<8}{karakter:<10}")

    return "".join(hasil)


def menu_rsa():
    kunci = None
    while True:
        judul("MENU RSA")
        print("1. Generate Kunci (input p, q, e sendiri)")
        print("2. Enkripsi")
        print("3. Dekripsi")
        print("4. Kembali ke Menu Utama")
        pilihan = input("\nPilih menu (1-4): ").strip()

        if pilihan == "1":
            kunci = rsa_buat_kunci()
            jeda()

        elif pilihan == "2":
            if kunci is None:
                print("[ERROR] Belum ada kunci. Silakan generate kunci dahulu (menu 1).")
                jeda()
                continue
            plaintext = input("\nMasukkan plaintext: ")
            hasil = rsa_encrypt(plaintext, kunci["e"], kunci["n"])
            if hasil is not None:
                print("\nHASIL AKHIR")
                garis()
                print(f"Plaintext  : {plaintext}")
                print(f"Kunci Publik (e, n) : ({kunci['e']}, {kunci['n']})")
                print(f"Ciphertext : {hasil}")
            jeda()

        elif pilihan == "3":
            if kunci is None:
                print("[ERROR] Belum ada kunci. Silakan generate kunci dahulu (menu 1).")
                jeda()
                continue
            teks_cipher = input("\nMasukkan ciphertext (angka dipisah spasi): ")
            try:
                daftar_cipher = [int(x) for x in teks_cipher.replace(",", " ").split()]
            except ValueError:
                print("[ERROR] Format ciphertext tidak valid!")
                jeda()
                continue
            hasil = rsa_decrypt(daftar_cipher, kunci["d"], kunci["n"])
            print("\nHASIL AKHIR")
            garis()
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

def menu_utama():
    judul("APLIKASI ENKRIPSI & DEKRIPSI (XOR CIPHER & RSA)")
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
            print("\nTerima kasih telah menggunakan aplikasi ini.")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")
            jeda()


if __name__ == "__main__":
    menu_utama()