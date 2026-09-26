"""
=======================================================================
 APLIKASI ENKRIPSI & DEKRIPSI - CAESAR CIPHER
 Kunci (pergeseran) diinput sendiri oleh user
=======================================================================
"""


def garis():
    print("-" * 65)


def judul(teks):
    print("=" * 65)
    print(teks.center(65))
    print("=" * 65)


def jeda():
    input("\nTekan ENTER untuk melanjutkan...")


# =======================================================================
# CAESAR CIPHER
# =======================================================================

def geser_karakter(ch, kunci):
    """
    Menggeser satu karakter sejauh 'kunci' posisi.
    - Huruf besar (A-Z) tetap huruf besar, huruf kecil (a-z) tetap huruf kecil.
    - Karakter selain huruf (spasi, angka, simbol) tidak diubah.
    """
    if ch.isupper():
        awal = ord('A')
        return chr((ord(ch) - awal + kunci) % 26 + awal)
    elif ch.islower():
        awal = ord('a')
        return chr((ord(ch) - awal + kunci) % 26 + awal)
    else:
        return ch  # karakter non-huruf tidak digeser


def caesar_process(teks, kunci, mode):
    pergeseran = kunci if mode == "ENKRIPSI" else -kunci

    print(f"\nProses {mode} (geser {'maju' if mode == 'ENKRIPSI' else 'mundur'} {kunci} huruf):")
    print(f"{'No':<4}{'Karakter':<10}{'Posisi Awal':<14}{'Hasil Geser':<14}{'Karakter Hasil':<16}")
    garis()

    hasil = []
    for i, ch in enumerate(teks):
        if ch.isalpha():
            awal = ord('A') if ch.isupper() else ord('a')
            posisi_awal = ord(ch) - awal
            posisi_hasil = (posisi_awal + pergeseran) % 26
            ch_hasil = chr(posisi_hasil + awal)
            print(f"{i+1:<4}{ch:<10}{posisi_awal:<14}{posisi_hasil:<14}{ch_hasil:<16}")
        else:
            ch_hasil = ch
            print(f"{i+1:<4}{repr(ch):<10}{'-':<14}{'-':<14}{repr(ch_hasil):<16}")
        hasil.append(ch_hasil)

    return "".join(hasil)


def input_kunci():
    """Minta input kunci (pergeseran), harus bilangan bulat 1-25."""
    while True:
        teks = input("Masukkan kunci pergeseran (1-25): ").strip()
        if not (teks.lstrip("-").isdigit()):
            print("[ERROR] Harus berupa angka!")
            continue
        kunci = int(teks)
        if not (1 <= kunci <= 25):
            print("[ERROR] Kunci harus di antara 1 dan 25!")
            continue
        return kunci


def menu_caesar_encrypt():
    judul("CAESAR CIPHER - ENKRIPSI")
    plaintext = input("Masukkan plaintext: ")
    kunci = input_kunci()

    hasil = caesar_process(plaintext, kunci, "ENKRIPSI")

    print("\nHASIL AKHIR")
    garis()
    print(f"Plaintext  : {plaintext}")
    print(f"Kunci      : {kunci}")
    print(f"Ciphertext : {hasil}")


def menu_caesar_decrypt():
    judul("CAESAR CIPHER - DEKRIPSI")
    ciphertext = input("Masukkan ciphertext: ")
    kunci = input_kunci()

    hasil = caesar_process(ciphertext, kunci, "DEKRIPSI")

    print("\nHASIL AKHIR")
    garis()
    print(f"Ciphertext : {ciphertext}")
    print(f"Kunci      : {kunci}")
    print(f"Plaintext  : {hasil}")


def menu_bruteforce():
    """Menampilkan semua kemungkinan kunci (1-25) untuk membantu analisis."""
    judul("BRUTE FORCE - COBA SEMUA KUNCI (1-25)")
    ciphertext = input("Masukkan ciphertext: ")

    print(f"\n{'Kunci':<8}{'Hasil':<40}")
    garis()
    for kunci in range(1, 26):
        pergeseran = -kunci
        hasil = []
        for ch in ciphertext:
            if ch.isalpha():
                awal = ord('A') if ch.isupper() else ord('a')
                posisi_hasil = (ord(ch) - awal + pergeseran) % 26
                hasil.append(chr(posisi_hasil + awal))
            else:
                hasil.append(ch)
        print(f"{kunci:<8}{''.join(hasil):<40}")


def menu_caesar():
    while True:
        judul("MENU CAESAR CIPHER")
        print("1. Enkripsi")
        print("2. Dekripsi")
        print("3. Brute Force (coba semua kunci 1-25)")
        print("4. Keluar")
        pilihan = input("\nPilih menu (1-4): ").strip()

        if pilihan == "1":
            menu_caesar_encrypt()
            jeda()
        elif pilihan == "2":
            menu_caesar_decrypt()
            jeda()
        elif pilihan == "3":
            menu_bruteforce()
            jeda()
        elif pilihan == "4":
            print("\nTerima kasih telah menggunakan aplikasi ini.")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")
            jeda()


if __name__ == "__main__":
    menu_caesar()