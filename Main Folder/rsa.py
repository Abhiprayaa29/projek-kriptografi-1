#APLIKASI RSA CHIPER

import math

import pandas as pd
import streamlit as st


# =======================================================================
# LOGIKA RSA (identik dengan versi CLI: is_prima, gcd, extended_gcd, dst.)
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
# TAMPILAN STREAMLIT
# =======================================================================

st.set_page_config(page_title="RSA Cipher", page_icon="🔑", layout="wide")

st.title("🔑 RSA Cipher")
st.caption("Enkripsi & Dekripsi asimetris — kunci publik untuk mengenkripsi, kunci privat untuk mendekripsi.")

if "rsa_key" not in st.session_state:
    st.session_state.rsa_key = None

# -----------------------------------------------------------------
# BAGIAN 1 : PEMBANGKITAN KUNCI (p, q input manual + validasi)
# -----------------------------------------------------------------
st.header("1️⃣ Pembangkitan Kunci")

col1, col2 = st.columns(2)
with col1:
    p_input = st.text_input("Masukkan p (bilangan prima)", key="p_input")
with col2:
    q_input = st.text_input("Masukkan q (bilangan prima)", key="q_input")

p_valid = q_valid = False
p = q = None

if p_input:
    if not p_input.isdigit():
        st.error("p harus berupa angka!")
    else:
        p = int(p_input)
        if not is_prima(p):
            st.error(f"{p} bukan bilangan prima! Silakan masukkan ulang.")
        else:
            p_valid = True

if q_input:
    if not q_input.isdigit():
        st.error("q harus berupa angka!")
    else:
        q = int(q_input)
        if not is_prima(q):
            st.error(f"{q} bukan bilangan prima! Silakan masukkan ulang.")
        elif p_valid and q == p:
            st.error("q tidak boleh sama dengan p!")
        else:
            q_valid = True

n = phi = None
e_valid = False
e = None

if p_valid and q_valid:
    n = p * q
    phi = (p - 1) * (q - 1)
    st.success(f"n = p × q = {p} × {q} = **{n}**")
    st.success(f"φ(n) = (p-1) × (q-1) = {p - 1} × {q - 1} = **{phi}**")

    e_input = st.text_input(
        f"Masukkan e (syarat: 2 s/d {phi - 1}, gcd(e, φ(n)) = 1)",
        key="e_input",
    )

    if e_input:
        if not e_input.isdigit():
            st.error("e harus berupa angka!")
        else:
            e = int(e_input)
            if e <= 1:
                st.error(
                    "e tidak boleh 1 atau kurang! Jika e=1, C = M^1 mod n = M "
                    "(tidak terjadi enkripsi). e minimal 2."
                )
            elif e >= phi:
                st.error(f"e harus lebih kecil dari φ(n) = {phi}!")
            elif gcd(e, phi) != 1:
                st.error(
                    f"e = {e} tidak coprime dengan φ(n) = {phi} "
                    f"(gcd({e}, {phi}) = {gcd(e, phi)}, harus = 1). Pilih e lain!"
                )
            else:
                e_valid = True

    if e_valid and st.button("🔧 Buat Kunci", type="primary"):
        d = modinv(e, phi)
        st.session_state.rsa_key = {"p": p, "q": q, "n": n, "phi": phi, "e": e, "d": d}
        st.rerun()

if st.session_state.rsa_key:
    kunci = st.session_state.rsa_key
    st.markdown("### ✅ Kunci Berhasil Dibuat")
    c1, c2 = st.columns(2)
    with c1:
        st.info(f"**Public Key**  (e, n) = ({kunci['e']}, {kunci['n']})")
    with c2:
        st.warning(f"**Private Key**  (d, n) = ({kunci['d']}, {kunci['n']})")
    if st.button("🗑️ Reset Kunci"):
        st.session_state.rsa_key = None
        st.rerun()

st.divider()

# -----------------------------------------------------------------
# BAGIAN 2 : ENKRIPSI
# -----------------------------------------------------------------
st.header("2️⃣ Enkripsi")

if not st.session_state.rsa_key:
    st.info("Buat kunci terlebih dahulu di Bagian 1.")
else:
    kunci = st.session_state.rsa_key
    plaintext = st.text_input("Masukkan plaintext", key="rsa_plaintext")
    if st.button("Enkripsi", key="btn_enkripsi", type="primary"):
        if not plaintext:
            st.error("Plaintext tidak boleh kosong!")
        else:
            hasil, tabel_proses, error = rsa_encrypt(plaintext, kunci["e"], kunci["n"])
            if tabel_proses:
                st.dataframe(pd.DataFrame(tabel_proses), use_container_width=True, hide_index=True)
            if error:
                st.error(error)
            else:
                st.success(f"Ciphertext: `{hasil}`")
                st.caption("Salin daftar angka di atas untuk didekripsi kembali di Bagian 3.")

st.divider()

# -----------------------------------------------------------------
# BAGIAN 3 : DEKRIPSI
# -----------------------------------------------------------------
st.header("3️⃣ Dekripsi")

if not st.session_state.rsa_key:
    st.info("Buat kunci terlebih dahulu di Bagian 1.")
else:
    kunci = st.session_state.rsa_key
    ciphertext_input = st.text_input(
        "Masukkan ciphertext (angka dipisah spasi atau koma)", key="rsa_ciphertext"
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
                plaintext_hasil, tabel_proses = rsa_decrypt(daftar_cipher, kunci["d"], kunci["n"])
                st.dataframe(pd.DataFrame(tabel_proses), use_container_width=True, hide_index=True)
                st.success(f"Plaintext: `{plaintext_hasil}`")

with st.expander("ℹ️ Cara Kerja RSA"):
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

        ⚠️ Catatan: pastikan nilai ASCII karakter plaintext **selalu lebih kecil dari n**,
        kalau tidak enkripsi akan gagal (pilih p, q yang lebih besar).
        """
    )