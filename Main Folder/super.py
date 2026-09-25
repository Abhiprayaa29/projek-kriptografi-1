"""
====================================================================
APLIKASI SUPER ENKRIPSI
4 Algoritma Berlapis: Caesar -> Vigenere -> XOR -> RSA

Enkripsi : Plaintext -> Caesar -> Vigenere -> XOR(bytes) -> RSA -> Angka
Dekripsi : Angka -> RSA -> XOR -> Vigenere -> Caesar -> Plaintext

Jalankan: streamlit run app.py
====================================================================
"""

import streamlit as st

# ====================================================================
# 1. CAESAR CIPHER
# Geser huruf sejauh `shift`. decrypt=True -> geser ke arah sebaliknya.
# ====================================================================

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


# ====================================================================
# 2. VIGENERE CIPHER
# Sama seperti Caesar, tapi shift-nya mengikuti huruf kunci yang diulang.
# Indeks kunci hanya maju saat bertemu huruf pada teks.
# ====================================================================

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


# ====================================================================
# 3. XOR CIPHER
# Teks -> bytes UTF-8, tiap byte di-XOR dengan byte kunci (berulang).
# XOR simetris: fungsi yang sama dipakai untuk enkripsi & dekripsi.
# ====================================================================

def xor_bytes(data: bytes, key: str) -> bytes:
    if not key:
        raise ValueError("Kunci XOR tidak boleh kosong.")
    kb = key.encode("utf-8")
    return bytes(b ^ kb[i % len(kb)] for i, b in enumerate(data))


# ====================================================================
# 4. RSA CIPHER
# Tiap byte (0-255) dienkripsi satu-satu: C = M^e mod n | M = C^d mod n
# ====================================================================

def rsa_encrypt(data: bytes, e: int, n: int) -> list:
    return [pow(b, e, n) for b in data]


def rsa_decrypt(numbers: list, d: int, n: int) -> bytes:
    out = bytearray()
    for c in numbers:
        m = pow(c, d, n)
        if m > 255:
            raise ValueError(f"Byte hasil dekripsi RSA = {m} (>255). Kunci RSA kemungkinan salah.")
        out.append(m)
    return bytes(out)


# ---- Pendukung pembuatan kunci RSA ----

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


# ====================================================================
# 5. FUNGSI GABUNGAN: SUPER ENKRIPSI / SUPER DEKRIPSI
# Menjalankan 4 tahap berurutan, mengembalikan hasil tiap tahap
# supaya bisa ditampilkan step-by-step.
# ====================================================================

def super_encrypt(plaintext, shift, vig_key, xor_key, e, n):
    step1 = caesar(plaintext, shift)
    step2 = vigenere(step1, vig_key)
    step3 = xor_bytes(step2.encode("utf-8"), xor_key)
    step4 = rsa_encrypt(step3, e, n)
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

    step1 = rsa_decrypt(angka, d, n)
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


# ====================================================================
# 6. ANTARMUKA STREAMLIT
# ====================================================================

st.set_page_config(page_title="Super Enkripsi", layout="wide")
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

                st.markdown("### Proses Bertahap")
                with st.expander("Tahap 1 - Caesar"):
                    st.write(f"Shift = {int(shift)}")
                    st.code(r["plaintext"])
                    st.code(r["caesar"])
                with st.expander("Tahap 2 - Vigenere"):
                    st.write(f"Kunci = {vig_key}")
                    st.code(r["vigenere"])
                with st.expander("Tahap 3 - XOR (byte)"):
                    st.write(f"Kunci = {xor_key}")
                    st.write("Hex:")
                    st.code(hex_view(r["xor_bytes"]))
                    st.write("Desimal:")
                    st.code(dec_view(r["xor_bytes"]))
                with st.expander("Tahap 4 - RSA"):
                    st.write(f"e = {e}, n = {n}  |  C = M^e mod n")
                    st.code(r["ciphertext"])
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