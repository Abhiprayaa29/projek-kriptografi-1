"""
=======================================================================
 APLIKASI ENKRIPSI & DEKRIPSI - XOR CIPHER (Streamlit)
 Jalankan dengan: streamlit run xor_streamlit.py
=======================================================================
"""

import streamlit as st
import pandas as pd


# =======================================================================
# LOGIKA XOR CIPHER (alurnya sama seperti versi CLI: xor_process dkk.)
# =======================================================================

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


def xor_process(data, key, mode):
    """
    data : list of int (nilai byte 0-255)
    key  : string kunci (tiap karakter diubah ke ASCII, lalu diulang jika lebih pendek)
    mode : "ENKRIPSI" atau "DEKRIPSI" (hanya label, prosesnya identik)

    Return: (hasil, tabel_proses)
      hasil        : list of int hasil XOR
      tabel_proses : list of dict, satu baris per byte, untuk ditampilkan sebagai tabel
    """
    key_bytes = [ord(k) for k in key]
    hasil = []
    tabel_proses = []

    for i, b in enumerate(data):
        k = key_bytes[i % len(key_bytes)]
        x = b ^ k

        hasil.append(x)
        tabel_proses.append({
            "No": i + 1,
            "Input (dec)": b,
            "Input (biner)": format(b, "08b"),
            "Key (dec)": k,
            "Key (biner)": format(k, "08b"),
            "XOR (dec)": x,
            "XOR (biner)": format(x, "08b"),
            "XOR (hex)": format(x, "02x"),
            "Karakter Hasil": byte_ke_karakter_aman(x),
        })

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
# TAMPILAN STREAMLIT
# =======================================================================

st.set_page_config(page_title="XOR Cipher", page_icon="🔐", layout="wide")

st.title("🔐 XOR Cipher")
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
key = st.text_input("Masukkan Key", placeholder="contoh: KEY (key selalu berupa teks/huruf)")

proses = st.button("🚀 Proses", type="primary")

if proses:
    if not data_input:
        st.error("Data tidak boleh kosong!")
    elif not key:
        st.error("Key tidak boleh kosong!")
    else:
        try:
            data_bytes = parse_input_ke_bytes(data_input, format_input)
        except ValueError as e:
            st.error(f"[ERROR] {e}")
        else:
            hasil, tabel_proses = xor_process(data_bytes, key, mode.upper())
            teks_hasil, biner_hasil, hex_hasil = hasil_ke_3_format(hasil)

            st.subheader(f"📋 Proses {mode} (setiap byte di-XOR dengan key secara berulang)")
            st.dataframe(pd.DataFrame(tabel_proses), use_container_width=True, hide_index=True)

            st.subheader("✅ Hasil Akhir — 3 Bentuk Output")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("**🔤 Huruf (Teks)**")
                st.code(teks_hasil if teks_hasil else "(kosong)", language=None)
            with c2:
                st.markdown("**0️⃣1️⃣ Biner**")
                st.code(biner_hasil, language=None)
            with c3:
                st.markdown("**# Heksadesimal**")
                st.code(hex_hasil, language=None)

            st.info(
                "Karakter yang tidak bisa dicetak (karakter kontrol) ditampilkan sebagai kode escape, "
                "misalnya `\\x03`. Gunakan bentuk **Biner** atau **Heksadesimal** untuk menyalin hasil dengan aman."
            )

with st.expander("ℹ️ Cara Kerja XOR Cipher"):
    st.markdown(
        """
        - **Enkripsi**: `Plaintext ⊕ Key = Ciphertext`
        - **Dekripsi**: `Ciphertext ⊕ Key = Plaintext` (pakai key yang sama)
        - Kalau key lebih pendek dari data, key akan **diulang** (`key[i % panjang_key]`).
        - Setiap byte data & key diubah dulu ke bentuk biner, baru di-XOR bit per bit.
        - **Key selalu dimasukkan sebagai teks** (tiap karakternya diubah ke ASCII terlebih dulu),
          tapi **data** yang diproses boleh dalam bentuk Teks, Biner, atau Heksadesimal.
        """
    )