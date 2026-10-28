"""
====================================================================
GABUNGAN SEMUA METODE - Streamlit App
Caesar Cipher | Vigenere Cipher | XOR Cipher | RSA Cipher | Super Enkripsi

Gabungan dari caesar.py, vigenere.py, xor.py, rsa.py, dan super.py.
Pilih metode lewat sidebar, lalu gunakan seperti aplikasi aslinya.

Jalankan: streamlit run gabungan.py
====================================================================
"""

import math

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Kriptografi - Semua Metode", layout="wide")


# =======================================================================
# LOGIKA CAESAR CIPHER
# =======================================================================

def geser_karakter(ch: str, kunci: int) -> str:
    if ch.isupper():
        awal = ord('A')
        return chr((ord(ch) - awal + kunci) % 26 + awal)
    elif ch.islower():
        awal = ord('a')
        return chr((ord(ch) - awal + kunci) % 26 + awal)
    else:
        return ch  # karakter non-huruf tidak digeser


def caesar_process(teks: str, kunci: int, mode: str):
    pergeseran = kunci if mode == "ENKRIPSI" else -kunci

    hasil = []
    detail = []
    for i, ch in enumerate(teks):
        if ch.isalpha():
            awal = ord('A') if ch.isupper() else ord('a')
            posisi_awal = ord(ch) - awal
            posisi_hasil = (posisi_awal + pergeseran) % 26
            ch_hasil = chr(posisi_hasil + awal)
            detail.append({
                "No": i + 1,
                "Karakter": ch,
                "Posisi Awal": posisi_awal,
                "Hasil Geser": posisi_hasil,
                "Karakter Hasil": ch_hasil,
            })
        else:
            ch_hasil = ch
            detail.append({
                "No": i + 1,
                "Karakter": repr(ch),
                "Posisi Awal": "-",
                "Hasil Geser": "-",
                "Karakter Hasil": repr(ch_hasil),
            })
        hasil.append(ch_hasil)

    return "".join(hasil), detail


def bruteforce_semua_kunci(ciphertext: str):
    """Mengembalikan daftar (kunci, hasil) untuk kunci 1-25."""
    daftar = []
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
        daftar.append({"Kunci": kunci, "Hasil": "".join(hasil)})
    return daftar


# =======================================================================
# LOGIKA VIGENERE CIPHER
# =======================================================================

def vigenere_process(text: str, key: str, decrypt: bool = False):
    """Mengembalikan (hasil, detail) per karakter untuk ditampilkan."""
    key = "".join(c for c in key if c.isalpha())
    if not key:
        raise ValueError("Kunci Vigenere harus berisi minimal satu huruf.")

    hasil = []
    detail = []
    idx = 0
    for i, ch in enumerate(text, start=1):
        if ch.isalpha():
            kunci_ch = key[idx % len(key)]
            geser = ord(kunci_ch.upper()) - ord('A')
            base = ord('A') if ch.isupper() else ord('a')
            posisi_awal = ord(ch) - base
            arah = -geser if decrypt else geser
            posisi_hasil = (posisi_awal + arah) % 26
            ch_hasil = chr(posisi_hasil + base)
            detail.append({
                "No": i,
                "Karakter": ch,
                "Kunci": kunci_ch,
                "Posisi Awal": posisi_awal,
                "Geseran": arah,
                "Posisi Hasil": posisi_hasil,
                "Karakter Hasil": ch_hasil,
            })
            hasil.append(ch_hasil)
            idx += 1
        else:
            hasil.append(ch)
            detail.append({
                "No": i,
                "Karakter": repr(ch),
                "Kunci": "-",
                "Posisi Awal": "-",
                "Geseran": "-",
                "Posisi Hasil": "-",
                "Karakter Hasil": repr(ch),
            })
    return "".join(hasil), detail


def vigenere(text: str, key: str, decrypt: bool = False) -> str:
    hasil, _ = vigenere_process(text, key, decrypt=decrypt)
    return hasil


def vigenere_encrypt(text: str, key: str) -> str:
    return vigenere(text, key, decrypt=False)


def vigenere_decrypt(text: str, key: str) -> str:
    return vigenere(text, key, decrypt=True)


# =======================================================================
# LOGIKA XOR CIPHER
# =======================================================================

def parse_input_ke_bytes(teks, format_input):
    """
    Mengubah input user menjadi list byte (int 0-255),
    sesuai format yang dipilih.
    format_input : "Teks" | "Biner" | "Heksadesimal"
    """
    teks = teks.strip()

    if format_input == "Teks":
        return [ord(c) for c in teks]

    elif format_input == "Biner":
        bersih = teks.replace(" ", "")
        if len(bersih) % 8 != 0:
            raise ValueError("Panjang biner harus kelipatan 8 (1 byte = 8 bit)!")
        if any(c not in "01" for c in bersih):
            raise ValueError("Biner hanya boleh berisi angka 0 dan 1!")
        return [int(bersih[i:i + 8], 2) for i in range(0, len(bersih), 8)]

    elif format_input == "Heksadesimal":
        bersih = teks.replace(" ", "")
        return list(bytes.fromhex(bersih))

    else:
        raise ValueError("Format input tidak dikenali!")


def byte_ke_karakter_aman(nilai):
    """Kembalikan karakter kalau bisa dicetak,
    kalau tidak kembalikan kode escape aman."""
    ch = chr(nilai)
    return ch if ch.isprintable() else f"\\x{nilai:02x}"


def parse_key(key_str):
    """
    Menentukan cara key diperlakukan:
    - Kalau key HANYA berisi angka (mis. "13")  -> dianggap SATU nilai byte (0-255),
      nilai itu diulang terus untuk setiap posisi. Key tidak dipecah per digit.
    - Kalau key berupa teks/huruf (mis. "keyke") -> tiap karakter diubah ke ASCII
      masing-masing, lalu diulang sesuai panjang key seperti biasa.

    Return: (key_bytes, key_display, jenis)
      key_bytes   : list of int, nilai byte key yang dipakai untuk XOR
      key_display : list of str, representasi key untuk ditampilkan di tabel
                    (panjangnya sama dengan key_bytes, dipasangkan lewat modulo yang sama)
      jenis       : "Angka (1 byte)" atau "Teks (per karakter)" - untuk info ke user
    """
    key_str = key_str.strip()

    if key_str.isdigit():
        nilai = int(key_str)
        if not (0 <= nilai <= 255):
            raise ValueError("Key angka harus di antara 0 dan 255 (karena 1 byte = 8 bit, maksimal nilainya 255)!")
        return [nilai], [key_str], "Angka (1 byte, diulang terus)"

    else:
        return [ord(c) for c in key_str], list(key_str), "Teks (per karakter)"


def xor_process(data, key_bytes, key_display, mode, tampilkan_ascii_key=True):
    """
    data                : list of int (nilai byte 0-255) - data yang diproses
    key_bytes           : list of int - nilai byte key (dari parse_key)
    key_display         : list of str - representasi key untuk ditampilkan di tabel
    mode                : "ENKRIPSI" atau "DEKRIPSI" (hanya label, prosesnya identik)
    tampilkan_ascii_key : False kalau key berupa angka (Key == ASCII Key, jadi redundan
                          dan kolom "ASCII Key" disembunyikan, langsung ke Biner Key)

    Return: (hasil, tabel_proses)
      hasil        : list of int hasil XOR
      tabel_proses : list of dict, satu baris per byte, untuk ditampilkan sebagai tabel
    """
    hasil = []
    tabel_proses = []

    for i, b in enumerate(data):
        idx = i % len(key_bytes)
        k = key_bytes[idx]
        k_label = key_display[idx]
        x = b ^ k

        hasil.append(x)
        baris = {
            "No": i + 1,
            "Huruf": byte_ke_karakter_aman(b),
            "ASCII": b,
            "Biner": format(b, "08b"),
            "Key": k_label,
        }
        if tampilkan_ascii_key:
            baris["ASCII Key"] = k
        baris["Biner Key"] = format(k, "08b")
        baris["XOR (biner)"] = format(x, "08b")
        baris["Hasil (dec)"] = x
        baris["Hasil (hex)"] = format(x, "02x")
        baris["Hasil (karakter)"] = byte_ke_karakter_aman(x)
        tabel_proses.append(baris)

    return hasil, tabel_proses


def hasil_ke_3_format(hasil_list):
    """
    Mengubah list hasil (int) menjadi 3 bentuk output sekaligus:
    huruf (teks), biner, dan heksadesimal.
    """
    data_bytes = bytes(hasil_list)
    teks = "".join(byte_ke_karakter_aman(b) for b in hasil_list)
    biner = " ".join(format(b, "08b") for b in data_bytes)
    hexa = data_bytes.hex()
    return teks, biner, hexa


# =======================================================================
# LOGIKA RSA CIPHER (berbasis teks)
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


def rsa_encrypt(teks, e, n):
    """Return (hasil, tabel_proses, error). error None kalau sukses."""
    hasil = []
    tabel_proses = []
    for i, ch in enumerate(teks):
        m = ord(ch)
        if m >= n:
            return None, tabel_proses, (
                f"Karakter '{ch}' (ASCII {m}) >= n ({n}). Pilih p, q yang lebih besar!"
            )
        c = pow(m, e, n)
        hasil.append(c)
        tabel_proses.append({
            "No": i + 1,
            "Karakter": ch,
            "M (ASCII)": m,
            "Perhitungan": f"{m}^{e} mod {n}",
            "C": c,
        })
    return hasil, tabel_proses, None


def rsa_decrypt(daftar_cipher, d, n):
    hasil = []
    tabel_proses = []
    for i, c in enumerate(daftar_cipher):
        m = pow(c, d, n)
        karakter = chr(m)
        hasil.append(karakter)
        tabel_proses.append({
            "No": i + 1,
            "C": c,
            "Perhitungan": f"{c}^{d} mod {n}",
            "M (ASCII)": m,
            "Karakter": karakter,
        })
    return "".join(hasil), tabel_proses


# =======================================================================
# LOGIKA SUPER ENKRIPSI (4 algoritma berlapis)
# =======================================================================

def caesar(text: str, shift: int, decrypt: bool = False) -> str:
    if decrypt:
        shift = -shift
    shift %= 26
    hasil = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            hasil.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            hasil.append(ch)  # non-huruf tidak diubah
    return "".join(hasil)


def xor_bytes(data: bytes, key: str) -> bytes:
    if not key:
        raise ValueError("Kunci XOR tidak boleh kosong.")
    kb = key.encode("utf-8")
    return bytes(b ^ kb[i % len(kb)] for i, b in enumerate(data))


def rsa_encrypt_bytes(data: bytes, e: int, n: int) -> list:
    return [pow(b, e, n) for b in data]


def rsa_decrypt_bytes(numbers: list, d: int, n: int) -> bytes:
    out = bytearray()
    for c in numbers:
        m = pow(c, d, n)
        if m > 255:
            raise ValueError(f"Byte hasil dekripsi RSA = {m} (>255). Kunci RSA kemungkinan salah.")
        out.append(m)
    return bytes(out)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def hitung_kunci_rsa(p: int, q: int, e: int):
    """Hitung n, phi, d dari p, q, e. Return (n, phi, d, [pesan_error])."""
    errors = []
    if not is_prime(p):
        errors.append(f"p = {p} bukan bilangan prima.")
    if not is_prime(q):
        errors.append(f"q = {q} bukan bilangan prima.")
    if p == q:
        errors.append("p dan q tidak boleh sama.")
    if errors:
        return None, None, None, errors

    n = p * q
    phi = (p - 1) * (q - 1)

    if n <= 255:
        errors.append(f"n = {n} (<=255). n harus > 255 agar byte 0-255 tidak terpotong modulo.")

    if e <= 1 or e >= phi:
        errors.append(f"e = {e} harus berada di antara 1 dan phi(n) = {phi}.")
        return n, phi, None, errors

    try:
        d = pow(e, -1, phi)  # invers modular bawaan Python (>=3.8)
    except ValueError:
        errors.append(f"e = {e} tidak koprima dengan phi(n) = {phi} (tidak punya invers).")
        return n, phi, None, errors

    if errors:
        return n, phi, None, errors
    return n, phi, d, []


PRESET_RSA = {
    "Preset 1 (p=17, q=19)": (17, 19, 5),
    "Preset 2 (p=13, q=23)": (13, 23, 5),
    "Preset 3 (p=19, q=23)": (19, 23, 5),
}


def super_encrypt(plaintext, shift, vig_key, xor_key, e, n):
    step1 = caesar(plaintext, shift)
    step2 = vigenere(step1, vig_key)
    step3 = xor_bytes(step2.encode("utf-8"), xor_key)
    step4 = rsa_encrypt_bytes(step3, e, n)
    return {
        "plaintext": plaintext,
        "caesar": step1,
        "vigenere": step2,
        "xor_bytes": step3,
        "angka": step4,
        "ciphertext": " ".join(map(str, step4)),
    }


def super_decrypt(ciphertext, shift, vig_key, xor_key, d, n):
    token = ciphertext.split()
    if not token:
        raise ValueError("Ciphertext tidak boleh kosong.")
    for t in token:
        if not t.lstrip("-").isdigit():
            raise ValueError(f"Token '{t}' bukan angka. Ciphertext harus berupa angka dipisah spasi.")
    angka = [int(t) for t in token]

    step1 = rsa_decrypt_bytes(angka, d, n)
    step2 = xor_bytes(step1, xor_key)
    try:
        step2_text = step2.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("Gagal decode UTF-8. Kunci XOR/RSA atau ciphertext kemungkinan salah.")
    step3 = vigenere(step2_text, vig_key, decrypt=True)
    step4 = caesar(step3, shift, decrypt=True)

    return {
        "angka": angka,
        "rsa_bytes": step1,
        "xor_text": step2_text,
        "vigenere": step3,
        "plaintext": step4,
    }


def hex_view(data: bytes) -> str:
    return " ".join(f"{b:02X}" for b in data)


def dec_view(data: bytes) -> str:
    return " ".join(str(b) for b in data)


def super_xor_tabel(data: bytes, key: str) -> list:
    """Tabel proses XOR per byte untuk tampilan Super (kunci = UTF-8, sama seperti xor_bytes)."""
    kb = key.encode("utf-8")
    rows = []
    for i, b in enumerate(data, start=1):
        k = kb[(i - 1) % len(kb)]
        x = b ^ k
        rows.append(
            {
                "No": i,
                "Masukan (des)": b,
                "Biner Masukan": format(b, "08b"),
                "Kunci (des)": k,
                "Hasil XOR (des)": x,
                "Biner Hasil": format(x, "08b"),
            }
        )
    return rows


def super_rsa_tabel(m_list: list, c_list: list, nilai: int, n: int, mode: str) -> list:
    """Tabel proses RSA per byte untuk tampilan Super. mode = ENKRIPSI (M->C) atau DEKRIPSI (C->M)."""
    rows = []
    for i, (m, c) in enumerate(zip(m_list, c_list), start=1):
        if mode == "ENKRIPSI":
            rows.append({"No": i, "M (byte)": m, "Perhitungan": f"{m}^{nilai} mod {n}", "C": c})
        else:
            rows.append({"No": i, "C": c, "Perhitungan": f"{c}^{nilai} mod {n}", "M (byte)": m})
    return rows


# =======================================================================
# ANTARMUKA: CAESAR CIPHER
# =======================================================================

def ui_caesar():
    st.title("Caesar Cipher")
    st.caption("Enkripsi, dekripsi, dan brute force teks menggunakan Caesar Cipher.")

    tab_enkripsi, tab_dekripsi, tab_bruteforce = st.tabs(
        ["Enkripsi", "Dekripsi", "Brute Force"]
    )

    # -----------------------------------------------------------------
    # TAB ENKRIPSI
    # -----------------------------------------------------------------
    with tab_enkripsi:
        plaintext = st.text_area(
            "Masukkan plaintext", height=120, key="plain_enc",
            placeholder="Ketik atau tempel teks di sini..."
        )
        kunci_enc = st.number_input(
            "Kunci pergeseran (1-25)", min_value=1, max_value=25, value=3, step=1, key="kunci_enc"
        )
        if st.button("Proses Enkripsi", type="primary"):
            if not plaintext.strip():
                st.warning("Teks tidak boleh kosong.")
            else:
                hasil, detail = caesar_process(plaintext, int(kunci_enc), "ENKRIPSI")
                st.success("Berhasil dienkripsi")
                st.text_area("Ciphertext", value=hasil, height=100)
                st.download_button(
                    "Unduh hasil (.txt)", data=hasil,
                    file_name="ciphertext.txt", mime="text/plain",
                )
                with st.expander("Lihat detail proses per karakter"):
                    st.dataframe(pd.DataFrame(detail), use_container_width=True, hide_index=True)

    # -----------------------------------------------------------------
    # TAB DEKRIPSI
    # -----------------------------------------------------------------
    with tab_dekripsi:
        ciphertext_in = st.text_area(
            "Masukkan ciphertext", height=120, key="cipher_dec",
            placeholder="Ketik atau tempel teks di sini..."
        )
        kunci_dec = st.number_input(
            "Kunci pergeseran (1-25)", min_value=1, max_value=25, value=3, step=1, key="kunci_dec"
        )
        if st.button("Proses Dekripsi", type="primary"):
            if not ciphertext_in.strip():
                st.warning("Teks tidak boleh kosong.")
            else:
                hasil, detail = caesar_process(ciphertext_in, int(kunci_dec), "DEKRIPSI")
                st.success("Berhasil didekripsi")
                st.text_area("Plaintext", value=hasil, height=100)
                st.download_button(
                    "Unduh hasil (.txt)", data=hasil,
                    file_name="plaintext.txt", mime="text/plain",
                )
                with st.expander("Lihat detail proses per karakter"):
                    st.dataframe(pd.DataFrame(detail), use_container_width=True, hide_index=True)

    # -----------------------------------------------------------------
    # TAB BRUTE FORCE
    # -----------------------------------------------------------------
    with tab_bruteforce:
        st.write("Mencoba semua kemungkinan kunci (1-25) untuk membantu analisis ciphertext.")
        ciphertext_bf = st.text_area(
            "Masukkan ciphertext", height=120, key="cipher_bf",
            placeholder="Ketik atau tempel teks di sini..."
        )
        if st.button("Jalankan Brute Force", type="primary"):
            if not ciphertext_bf.strip():
                st.warning("Teks tidak boleh kosong.")
            else:
                daftar = bruteforce_semua_kunci(ciphertext_bf)
                st.dataframe(pd.DataFrame(daftar), use_container_width=True, hide_index=True)

    with st.expander("Cara kerja"):
        st.write(
            "Setiap huruf pada teks digeser sejauh nilai kunci di sepanjang alfabet. "
            "Karakter non-huruf seperti spasi, angka, dan tanda baca tidak diubah. "
            "Pada dekripsi, arah pergeseran dibalik (dikurangi, bukan ditambah). "
            "Fitur brute force mencoba seluruh kunci dari 1 sampai 25 sekaligus, "
            "berguna saat kunci yang benar tidak diketahui."
        )


# =======================================================================
# ANTARMUKA: VIGENERE CIPHER
# =======================================================================

def ui_vigenere():
    st.title("Vigenere Cipher")
    st.caption("Enkripsi dan dekripsi teks menggunakan Vigenere Cipher.")

    mode = st.radio("Pilih mode", ["Enkripsi", "Dekripsi"], horizontal=True)

    label_teks = "Masukkan plaintext" if mode == "Enkripsi" else "Masukkan ciphertext"
    teks = st.text_area(label_teks, height=150, placeholder="Ketik atau tempel teks di sini...")
    kunci = st.text_input("Masukkan kunci", placeholder="Contoh: KUNCI")

    col1, col2 = st.columns([1, 1])
    with col1:
        proses = st.button("Proses", type="primary", use_container_width=True)
    with col2:
        reset = st.button("Bersihkan", use_container_width=True)

    if reset:
        st.rerun()

    if proses:
        if not teks.strip():
            st.warning("Teks tidak boleh kosong.")
        elif not any(c.isalpha() for c in kunci):
            st.warning("Kunci harus berisi minimal satu huruf.")
        else:
            try:
                decrypt_mode = mode == "Dekripsi"
                hasil, detail = vigenere_process(teks, kunci, decrypt=decrypt_mode)
                if decrypt_mode:
                    st.success("Berhasil didekripsi")
                    st.text_area("Plaintext", value=hasil, height=150)
                else:
                    st.success("Berhasil dienkripsi")
                    st.text_area("Ciphertext", value=hasil, height=150)

                st.download_button(
                    label="Unduh hasil (.txt)",
                    data=hasil,
                    file_name="hasil_vigenere.txt",
                    mime="text/plain",
                )

                st.subheader(
                    "Tampilan Proses Dekripsi" if decrypt_mode
                    else "Tampilan Proses Enkripsi"
                )
                st.caption(
                    "Kolom Kunci = huruf kunci yang aktif pada posisi tersebut. "
                    "Geseran = nilai huruf kunci (0-25) untuk enkripsi, negatif untuk dekripsi. "
                    "Karakter non-huruf tidak diubah dan tidak menggeser posisi kunci."
                )
                with st.expander("Lihat detail proses per karakter", expanded=True):
                    st.dataframe(pd.DataFrame(detail), use_container_width=True, hide_index=True)
            except ValueError as e:
                st.error(f"Kesalahan: {e}")

    with st.expander("Cara kerja"):
        st.write(
            "Setiap huruf pada teks digeser sesuai huruf kunci yang berulang "
            "secara siklis. Karakter non-huruf seperti spasi, angka, dan tanda "
            "baca tidak diubah dan tidak menggeser posisi kunci. Besar-kecil "
            "huruf (kapital/huruf kecil) tetap dipertahankan."
        )


# =======================================================================
# ANTARMUKA: XOR CIPHER
# =======================================================================

def ui_xor():
    st.title("XOR Cipher")
    st.caption("Enkripsi & Dekripsi dengan operasi XOR - kunci yang sama dipakai untuk kedua arah (symmetric encryption).")

    mode = st.radio("Mode", ["Enkripsi", "Dekripsi"], horizontal=True)

    format_input = st.radio(
        "Format Input Data",
        ["Teks", "Biner", "Heksadesimal"],
        horizontal=True,
        help="Data (plaintext/ciphertext) boleh dimasukkan dalam bentuk teks biasa, biner, atau heksadesimal.",
    )

    contoh = {
        "Teks": "HELLO",
        "Biner": "01001000 01000101 01001100 01001100 01001111",
        "Heksadesimal": "48454c4c4f",
    }
    data_input = st.text_input(f"Masukkan Data ({format_input})", placeholder=f"contoh: {contoh[format_input]}")
    key = st.text_input(
        "Masukkan Key",
        placeholder="contoh: keyke (teks) atau 13 (angka = nilai byte tunggal)",
        help="Kalau diisi ANGKA saja (mis. 13), key dianggap satu nilai byte yang diulang terus. "
             "Kalau diisi HURUF/teks (mis. keyke), tiap karakternya dipakai bergantian sesuai posisinya.",
    )

    if key:
        try:
            _, _, jenis_key = parse_key(key)
            st.caption(f"Key terdeteksi sebagai: **{jenis_key}**")
        except ValueError as e:
            st.caption(f"{e}")

    proses = st.button("Proses", type="primary")

    if proses:
        if not data_input:
            st.error("Data tidak boleh kosong!")
        elif not key:
            st.error("Key tidak boleh kosong!")
        else:
            try:
                data_bytes = parse_input_ke_bytes(data_input, format_input)
                key_bytes, key_display, jenis_key = parse_key(key)
            except ValueError as e:
                st.error(f"[ERROR] {e}")
            else:
                hasil, tabel_proses = xor_process(
                    data_bytes, key_bytes, key_display, mode.upper(),
                    tampilkan_ascii_key=(jenis_key != "Angka (1 byte, diulang terus)"),
                )
                teks_hasil, biner_hasil, hex_hasil = hasil_ke_3_format(hasil)

                st.subheader(f"Proses {mode} (setiap byte di-XOR dengan key secara berulang)")
                st.dataframe(pd.DataFrame(tabel_proses), use_container_width=True, hide_index=True)

                st.subheader("Hasil Akhir - 3 Bentuk Output")
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown("**Huruf (Teks)**")
                    st.code(teks_hasil if teks_hasil else "(kosong)", language=None)
                with c2:
                    st.markdown("**Biner**")
                    st.code(biner_hasil, language=None)
                with c3:
                    st.markdown("**# Heksadesimal**")
                    st.code(hex_hasil, language=None)

                st.info(
                    "Karakter yang tidak bisa dicetak (karakter kontrol) ditampilkan sebagai kode escape, "
                    "misalnya `\\x03`. Gunakan bentuk **Biner** atau **Heksadesimal** untuk menyalin hasil dengan aman."
                )

    with st.expander("Cara Kerja XOR Cipher"):
        st.markdown(
            """
            - **Enkripsi**: `Plaintext ⊕ Key = Ciphertext`
            - **Dekripsi**: `Ciphertext ⊕ Key = Plaintext` (pakai key yang sama)
            - Kalau key lebih pendek dari data, key akan **diulang** (`key[i % panjang_key]`).
            - Setiap byte data & key diubah dulu ke bentuk biner, baru di-XOR bit per bit.
            - **Key angka (mis. `13`)** → dianggap **satu nilai byte** yang diulang terus untuk semua posisi.
            - **Key huruf/teks (mis. `keyke`)** → tiap karakternya diubah ke ASCII masing-masing,
              lalu dipakai bergantian sesuai posisi (dan diulang kalau key lebih pendek dari data).
            - **Data** yang diproses boleh dalam bentuk Teks, Biner, atau Heksadesimal.
            """
        )


# =======================================================================
# ANTARMUKA: RSA CIPHER
# =======================================================================

def ui_rsa():
    st.title("RSA Cipher")
    st.caption("Enkripsi & Dekripsi asimetris - kunci publik untuk mengenkripsi, kunci privat untuk mendekripsi.")

    # ---------------------- Kunci ----------------------
    st.header("1. Kunci RSA")

    mode_key = st.radio(
        "Mode kunci",
        ["Preset Otomatis", "Manual (p, q, e)"],
        horizontal=True,
        help="Preset langsung menghasilkan kunci; Manual memilih p, q, dan e sendiri.",
    )

    if mode_key == "Preset Otomatis":
        pilihan = st.selectbox("Pilih preset", list(PRESET_RSA.keys()))
        p, q, e = PRESET_RSA[pilihan]
    else:
        c1, c2, c3 = st.columns(3)
        p = int(c1.number_input("p (prima)", min_value=2, value=17, step=1))
        q = int(c2.number_input("q (prima)", min_value=2, value=19, step=1))
        e = int(c3.number_input("e (harus koprima dengan φ(n))", min_value=2, value=5, step=1))

    n, phi, d, errors = hitung_kunci_rsa(int(p), int(q), int(e))

    kunci = None
    if errors:
        for err in errors:
            st.error(err)
    elif d is None:
        st.error("Kunci privat d tidak bisa dihitung. Periksa nilai e.")
    else:
        kunci = {"p": int(p), "q": int(q), "n": n, "phi": phi, "e": int(e), "d": d}
        st.success(
            f"n = {int(p)} × {int(q)} = **{n}** | φ(n) = ({int(p)} - 1) × ({int(q)} - 1) = **{phi}** | "
            f"d = invers modular dari {int(e)} mod {phi} = **{d}**"
        )
        k1, k2 = st.columns(2)
        k1.info(f"**Public Key (e, n)** = ({int(e)}, {n}) - dipakai untuk enkripsi")
        k2.warning(f"**Private Key (d, n)** = ({d}, {n}) - dipakai untuk dekripsi")

    st.divider()

    # ---------------------- Enkripsi / Dekripsi ----------------------
    st.header("2. Enkripsi & Dekripsi")

    if kunci is None:
        st.info("Perbaiki kunci RSA di bagian 1 terlebih dahulu.")
    else:
        tab_enc, tab_dec = st.tabs(["Enkripsi", "Dekripsi"])

        with tab_enc:
            plaintext = st.text_area("Masukkan plaintext", height=100, key="rsa_plaintext")
            if st.button("Enkripsi", key="btn_enkripsi", type="primary"):
                if not plaintext:
                    st.error("Plaintext tidak boleh kosong!")
                else:
                    hasil, tabel_proses, error = rsa_encrypt(plaintext, kunci["e"], kunci["n"])
                    if tabel_proses:
                        st.write("**Proses per karakter:**")
                        st.dataframe(pd.DataFrame(tabel_proses), use_container_width=True, hide_index=True)
                    if error:
                        st.error(error)
                    else:
                        st.success("Enkripsi berhasil!")
                        st.code(" ".join(map(str, hasil)), language="text")
                        st.caption("Salin daftar angka di atas ke tab Dekripsi.")

        with tab_dec:
            ciphertext_input = st.text_area(
                "Masukkan ciphertext (angka dipisah spasi atau koma)",
                height=100,
                key="rsa_ciphertext",
            )
            if st.button("Dekripsi", key="btn_dekripsi", type="primary"):
                if not ciphertext_input:
                    st.error("Ciphertext tidak boleh kosong!")
                else:
                    try:
                        daftar_cipher = [int(x) for x in ciphertext_input.replace(",", " ").split()]
                    except ValueError:
                        st.error("Format ciphertext tidak valid!")
                    else:
                        if not daftar_cipher:
                            st.error("Ciphertext tidak boleh kosong!")
                        else:
                            plaintext_hasil, tabel_proses = rsa_decrypt(daftar_cipher, kunci["d"], kunci["n"])
                            st.write("**Proses per angka:**")
                            st.dataframe(pd.DataFrame(tabel_proses), use_container_width=True, hide_index=True)
                            st.success("Dekripsi berhasil!")
                            st.code(plaintext_hasil, language="text")

    with st.expander("Cara Kerja RSA"):
        st.markdown(
            """
            1. Pilih dua bilangan prima **p** dan **q** (berbeda)
            2. Hitung **n = p × q**
            3. Hitung **φ(n) = (p-1)(q-1)**
            4. Pilih **e** dengan syarat `1 < e < φ(n)` dan `gcd(e, φ(n)) = 1`
            5. Hitung **d** = invers modular dari e terhadap φ(n), yaitu `e × d ≡ 1 (mod φ(n))`
            6. **Public Key = (e, n)** dipakai untuk enkripsi, **Private Key = (d, n)** dipakai untuk dekripsi
            7. Enkripsi: `C = M^e mod n`
            8. Dekripsi: `M = C^d mod n`

            Catatan: pastikan nilai ASCII karakter plaintext **selalu lebih kecil dari n**,
            kalau tidak enkripsi akan gagal (pilih p, q yang lebih besar).
            """
        )


# =======================================================================
# ANTARMUKA: SUPER ENKRIPSI
# =======================================================================

def ui_super():
    st.title("Super Enkripsi")
    st.caption("4 Algoritma Berlapis: Caesar -> Vigenere -> XOR -> RSA")
    st.markdown(
        "**Enkripsi:** `Plaintext -> Caesar -> Vigenere -> XOR -> RSA -> Angka`  \n"
        "**Dekripsi:** `Angka -> RSA -> XOR -> Vigenere -> Caesar -> Plaintext`"
    )
    st.divider()

    # ---------------------- Pengaturan Kunci ----------------------
    st.subheader("Pengaturan Kunci")

    with st.expander("Kunci Caesar, Vigenere, XOR", expanded=True):
        c1, c2, c3 = st.columns(3)
        shift = c1.number_input("Kunci Caesar (shift)", value=3, step=1)
        vig_key = c2.text_input("Kunci Vigenere (huruf)", value="KUNCI")
        xor_key = c3.text_input("Kunci XOR (teks bebas)", value="SECRET")

    with st.expander("Kunci RSA (n, e, d)", expanded=True):
        mode_rsa = st.radio("Metode kunci RSA:", ["Preset Otomatis", "Manual (p, q, e)"], horizontal=True)

        if mode_rsa == "Preset Otomatis":
            pilihan = st.selectbox("Pilih preset:", list(PRESET_RSA.keys()))
            p, q, e = PRESET_RSA[pilihan]
        else:
            c1, c2, c3 = st.columns(3)
            p = c1.number_input("p (prima)", min_value=2, value=17, step=1)
            q = c2.number_input("q (prima)", min_value=2, value=19, step=1)
            e = c3.number_input("e", min_value=2, value=5, step=1)

        n, phi, d, errors = hitung_kunci_rsa(int(p), int(q), int(e))
        rsa_valid = not errors
        if errors:
            for err in errors:
                st.error(err)
        else:
            st.success(f"n = {n}, phi(n) = {phi}, e = {e}, d = {d}")

    st.divider()

    # ---------------------- Mode Operasi ----------------------
    tab_enc, tab_dec = st.tabs(["Mode Enkripsi", "Mode Dekripsi"])

    with tab_enc:
        plaintext = st.text_area("Plaintext:", height=150, placeholder="Ketik teks yang ingin dienkripsi...")

        if st.button("Enkripsi Sekarang", type="primary"):
            if not plaintext:
                st.error("Plaintext tidak boleh kosong.")
            elif not vig_key.strip():
                st.error("Kunci Vigenere tidak boleh kosong.")
            elif not xor_key:
                st.error("Kunci XOR tidak boleh kosong.")
            elif not rsa_valid:
                st.error("Kunci RSA belum valid, perbaiki dahulu di atas.")
            else:
                try:
                    r = super_encrypt(plaintext, int(shift), vig_key, xor_key, e, n)
                    st.success("Enkripsi berhasil!")
                    st.markdown("### Ciphertext Final")
                    st.code(r["ciphertext"], language="text")

                    st.markdown("### Proses Enkripsi Bertahap")
                    st.caption("Urutan: Plaintext -> Caesar -> Vigenere -> XOR -> RSA. Tiap tahap memasukkan hasil tahap sebelumnya.")

                    with st.expander("Tahap 1 - Caesar Cipher (geser huruf)", expanded=True):
                        st.write(f"Menggeser tiap huruf ke kanan sejauh shift. Selain huruf tidak diubah. Rumus: `C = (M + shift) mod 26`, shift = {int(shift)}.")
                        st.write("**Masukan (plaintext):**")
                        st.code(r["plaintext"], language="text")
                        st.write("**Hasil Tahap 1 (Caesar):**")
                        st.code(r["caesar"], language="text")
                        st.write("Detail per karakter:")
                        _, detail1 = caesar_process(r["plaintext"], int(shift), "ENKRIPSI")
                        st.dataframe(pd.DataFrame(detail1), use_container_width=True, hide_index=True)

                    with st.expander("Tahap 2 - Vigenere Cipher (kunci huruf berulang)", expanded=True):
                        st.write(f"Tiap huruf digeser sesuai huruf kunci yang berulang siklis. Kunci: `{vig_key}`.")
                        st.write("**Masukan (hasil Tahap 1):**")
                        st.code(r["caesar"], language="text")
                        st.write("**Hasil Tahap 2 (Vigenere):**")
                        st.code(r["vigenere"], language="text")
                        st.write("Detail per karakter:")
                        _, detail2 = vigenere_process(r["caesar"], vig_key)
                        st.dataframe(pd.DataFrame(detail2), use_container_width=True, hide_index=True)

                    with st.expander("Tahap 3 - XOR (per byte)", expanded=True):
                        st.write(f"Hasil Tahap 2 diubah jadi byte UTF-8, lalu tiap byte di-XOR dengan byte kunci yang berulang. Kunci: `{xor_key}` = byte {list(xor_key.encode('utf-8'))}.")
                        st.write("**Masukan (teks hasil Tahap 2):**")
                        st.code(r["vigenere"], language="text")
                        st.write("Detail per byte (XOR: a ^ b = hasil):")
                        st.dataframe(
                            pd.DataFrame(super_xor_tabel(r["vigenere"].encode("utf-8"), xor_key)),
                            use_container_width=True,
                            hide_index=True,
                        )

                    with st.expander("Tahap 4 - RSA (per byte)", expanded=True):
                        st.write(f"Tiap byte dienkripsi dengan rumus `C = M^e mod n`, e = {e}, n = {n}.")
                        st.write("**Masukan (byte Tahap 3, hex):**")
                        st.code(hex_view(r["xor_bytes"]), language="text")
                        st.write("Detail per byte:")
                        st.dataframe(
                            pd.DataFrame(super_rsa_tabel(r["xor_bytes"], r["angka"], e, n, "ENKRIPSI")),
                            use_container_width=True,
                            hide_index=True,
                        )
                        st.write("**Hasil Tahap 4 (ciphertext):**")
                        st.code(r["ciphertext"], language="text")
                except ValueError as err:
                    st.error(f"Kesalahan: {err}")

    with tab_dec:
        ciphertext = st.text_area("Ciphertext (angka dipisah spasi):", height=150, placeholder="Contoh: 227 79 197")

        if st.button("Dekripsi Sekarang", type="primary"):
            if not ciphertext.strip():
                st.error("Ciphertext tidak boleh kosong.")
            elif not vig_key.strip():
                st.error("Kunci Vigenere tidak boleh kosong.")
            elif not xor_key:
                st.error("Kunci XOR tidak boleh kosong.")
            elif not rsa_valid:
                st.error("Kunci RSA belum valid, perbaiki dahulu di atas.")
            else:
                try:
                    r = super_decrypt(ciphertext, int(shift), vig_key, xor_key, d, n)
                    st.success("Dekripsi berhasil!")
                    st.markdown("### Plaintext Hasil Dekripsi")
                    st.code(r["plaintext"])

                    st.markdown("### Proses Bertahap")
                    with st.expander("Tahap 1 - Dekripsi RSA"):
                        st.write(f"d = {d}, n = {n}  |  M = C^d mod n")
                        st.write("Hex:")
                        st.code(hex_view(r["rsa_bytes"]))
                        st.write("Desimal:")
                        st.code(dec_view(r["rsa_bytes"]))
                    with st.expander("Tahap 2 - Dekripsi XOR"):
                        st.write(f"Kunci = {xor_key}")
                        st.code(r["xor_text"])
                    with st.expander("Tahap 3 - Dekripsi Vigenere"):
                        st.write(f"Kunci = {vig_key}")
                        st.code(r["vigenere"])
                    with st.expander("Tahap 4 - Dekripsi Caesar (Plaintext)"):
                        st.write(f"Shift = {int(shift)}")
                        st.code(r["plaintext"])
                except ValueError as err:
                    st.error(f"Kesalahan: {err}")

    with st.expander("Cara kerja"):
        st.write(
            "Super Enkripsi menggabungkan 4 algoritma secara berurutan dalam satu "
            "proses. Enkripsi berjalan: Caesar menggeser setiap huruf sejauh kunci, "
            "hasilnya lalu di-Vigenere dengan kunci huruf yang diulang, hasilnya "
            "diubah menjadi byte dan di-XOR dengan kunci XOR, lalu tiap byte "
            "dienkripsi RSA (C = M^e mod n) sehingga ciphertext akhir berupa daftar "
            "angka dipisah spasi. Dekripsi menjalankan urutan terbalik: RSA "
            "(M = C^d mod n) -> XOR -> Vigenere -> Caesar, sehingga menghasilkan "
            "plaintext kembali. Kunci yang sama dipakai di kedua arah: shift "
            "Caesar, kunci Vigenere, kunci XOR, dan pasangan (e, n) untuk enkripsi "
            "serta (d, n) untuk dekripsi. Setelah menekan tombol, bagian Proses "
            "Bertahap menampilkan hasil tiap lapis agar bisa ditelusuri satu per satu."
        )

    st.divider()


# =======================================================================
# ANTARMUKA GABUNGAN - PILIH METODE (sidebar)
# =======================================================================

st.sidebar.title("Kriptografi")
st.sidebar.caption("Pilih metode yang ingin digunakan.")

DAFTAR_METODE = [
    "Caesar Cipher",
    "Vigenere Cipher",
    "XOR Cipher",
    "RSA Cipher",
    "Super Enkripsi",
]

pilihan = st.sidebar.selectbox("Pilih Metode", DAFTAR_METODE)

if pilihan == "Caesar Cipher":
    ui_caesar()
elif pilihan == "Vigenere Cipher":
    ui_vigenere()
elif pilihan == "XOR Cipher":
    ui_xor()
elif pilihan == "RSA Cipher":
    ui_rsa()
elif pilihan == "Super Enkripsi":
    ui_super()
