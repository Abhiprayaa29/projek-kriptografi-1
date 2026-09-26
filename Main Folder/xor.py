
#APLIKASI XOR CHIPER

import streamlit as st
import pandas as pd


#LOGIKA XOR CHIPER

def parse_input_ke_bytes(teks, format_input):
    """
    Mengubah input user menjadi list byte (int 0-255), sesuai format yang dipilih.
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
    """Kembalikan karakter kalau bisa dicetak, kalau tidak kembalikan kode escape aman."""
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
      key_display : list of str, representasi key yang ditampilkan di tabel
                    (panjangnya sama dengan key_bytes, dipasangkan lewat modulo yang sama)
      jenis       : "Angka (1 byte)" atau "Teks (per karakter)" — untuk info ke user
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
    data                : list of int (nilai byte 0-255) — data yang diproses
    key_bytes           : list of int — nilai byte key (dari parse_key)
    key_display         : list of str — representasi key untuk ditampilkan di tabel
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


#tampilan streamlit

st.set_page_config(page_title="XOR Cipher", layout="wide")

st.title("XOR Cipher")
st.caption("Enkripsi & Dekripsi dengan operasi XOR — kunci yang sama dipakai untuk kedua arah (symmetric encryption).")

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

            st.subheader("Hasil Akhir — 3 Bentuk Output")
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