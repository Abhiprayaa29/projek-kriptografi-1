"""
====================================================================
VIGENERE CIPHER - Streamlit App
Aplikasi web sederhana untuk enkripsi & dekripsi Vigenere Cipher

Jalankan: streamlit run vigenere_app.py
====================================================================
"""

import streamlit as st


def vigenere(text: str, key: str, decrypt: bool = False) -> str:

    key = "".join(c for c in key if c.isalpha())
    if not key:
        raise ValueError("Kunci Vigenere harus berisi minimal satu huruf.")

    hasil = []
    idx = 0
    for ch in text:
        if ch.isalpha():
            geser = ord(key[idx % len(key)].upper()) - ord('A')
            base = ord('A') if ch.isupper() else ord('a')
            arah = -geser if decrypt else geser
            hasil.append(chr((ord(ch) - base + arah) % 26 + base))
            idx += 1
        else:
            hasil.append(ch)
    return "".join(hasil)


def vigenere_encrypt(text: str, key: str) -> str:
    return vigenere(text, key, decrypt=False)


def vigenere_decrypt(text: str, key: str) -> str:
    return vigenere(text, key, decrypt=True)


# ====================================================================
# ANTARMUKA STREAMLIT
# ====================================================================

st.set_page_config(page_title="Vigenere Cipher", layout="centered")

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
            if mode == "Enkripsi":
                hasil = vigenere_encrypt(teks, kunci)
                st.success("Berhasil dienkripsi")
                st.text_area("Ciphertext", value=hasil, height=150)
            else:
                hasil = vigenere_decrypt(teks, kunci)
                st.success("Berhasil didekripsi")
                st.text_area("Plaintext", value=hasil, height=150)

            st.download_button(
                label="Unduh hasil (.txt)",
                data=hasil,
                file_name="hasil_vigenere.txt",
                mime="text/plain",
            )
        except ValueError as e:
            st.error(f"Kesalahan: {e}")

with st.expander("Cara kerja"):
    st.write(
        "Setiap huruf pada teks digeser sesuai huruf kunci yang berulang "
        "secara siklis. Karakter non-huruf seperti spasi, angka, dan tanda "
        "baca tidak diubah dan tidak menggeser posisi kunci. Besar-kecil "
        "huruf (kapital/huruf kecil) tetap dipertahankan."
    )