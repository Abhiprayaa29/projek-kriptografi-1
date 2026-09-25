"""
==================================================================================
APLIKASI SUPER ENKRIPSI
Gabungan 4 Algoritma Berlapis: Caesar -> Vigenere -> XOR -> RSA
==================================================================================

Alur Enkripsi:
    Plaintext -> Caesar -> Vigenere -> XOR (bytes) -> RSA -> Ciphertext (angka)

Alur Dekripsi (inversi presisi, urutan terbalik):
    Ciphertext (angka) -> RSA -> XOR -> Vigenere -> Caesar -> Plaintext

Jalankan dengan:
    streamlit run app.py
==================================================================================
"""

import streamlit as st

# ==================================================================================
# BAGIAN 1: FUNGSI-FUNGSI MATEMATIKA PENDUKUNG (UNTUK RSA)
# ==================================================================================

def is_prime(n: int) -> bool:
    """Mengecek apakah suatu bilangan adalah bilangan prima."""
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


def gcd(a: int, b: int) -> int:
    """Mencari Greatest Common Divisor (FPB) dengan algoritma Euclid."""
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a: int, b: int):
    """Extended Euclidean Algorithm -> mengembalikan (gcd, x, y) sehingga a*x + b*y = gcd."""
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y


def mod_inverse(e: int, phi: int):
    """
    Mencari invers modular dari e terhadap phi, yaitu nilai d
    sehingga (e * d) mod phi = 1. Mengembalikan None jika tidak ada invers.
    """
    g, x, _ = extended_gcd(e, phi)
    if g != 1:
        return None  # invers tidak ada karena e dan phi tidak koprima
    return x % phi


# ==================================================================================
# BAGIAN 2: TAHAP 1 - CAESAR CIPHER
# Substitusi alfabet dengan pergeseran integer. Hanya huruf A-Z/a-z yang digeser,
# karakter lain (spasi, angka, simbol) dibiarkan apa adanya.
# ==================================================================================

def caesar_encrypt(text: str, shift: int) -> str:
    """Mengenkripsi teks dengan Caesar Cipher (geser maju sejauh `shift`)."""
    hasil = []
    shift = shift % 26
    for ch in text:
        if ch.isupper():
            hasil.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
        elif ch.islower():
            hasil.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
        else:
            hasil.append(ch)  # karakter non-alfabet tidak diubah
    return "".join(hasil)


def caesar_decrypt(text: str, shift: int) -> str:
    """Mendekripsi teks Caesar Cipher (geser mundur sejauh `shift`)."""
    return caesar_encrypt(text, -shift)


# ==================================================================================
# BAGIAN 3: TAHAP 2 - VIGENERE CIPHER
# Substitusi alfabet dengan kunci string berulang. Indeks kunci hanya maju ketika
# bertemu karakter alfabet pada teks, sehingga karakter non-alfabet tetap utuh.
# ==================================================================================

def _bersihkan_kunci_vigenere(key: str) -> str:
    """Mengambil hanya karakter alfabet dari kunci Vigenere."""
    return "".join(ch for ch in key if ch.isalpha())


def vigenere_encrypt(text: str, key: str) -> str:
    """Mengenkripsi teks dengan Vigenere Cipher."""
    key_bersih = _bersihkan_kunci_vigenere(key)
    if not key_bersih:
        raise ValueError("Kunci Vigenere harus mengandung minimal satu huruf alfabet.")

    hasil = []
    idx_key = 0
    for ch in text:
        if ch.isalpha():
            geser = ord(key_bersih[idx_key % len(key_bersih)].upper()) - ord('A')
            if ch.isupper():
                hasil.append(chr((ord(ch) - ord('A') + geser) % 26 + ord('A')))
            else:
                hasil.append(chr((ord(ch) - ord('a') + geser) % 26 + ord('a')))
            idx_key += 1
        else:
            hasil.append(ch)
    return "".join(hasil)


def vigenere_decrypt(text: str, key: str) -> str:
    """Mendekripsi teks Vigenere Cipher."""
    key_bersih = _bersihkan_kunci_vigenere(key)
    if not key_bersih:
        raise ValueError("Kunci Vigenere harus mengandung minimal satu huruf alfabet.")

    hasil = []
    idx_key = 0
    for ch in text:
        if ch.isalpha():
            geser = ord(key_bersih[idx_key % len(key_bersih)].upper()) - ord('A')
            if ch.isupper():
                hasil.append(chr((ord(ch) - ord('A') - geser) % 26 + ord('A')))
            else:
                hasil.append(chr((ord(ch) - ord('a') - geser) % 26 + ord('a')))
            idx_key += 1
        else:
            hasil.append(ch)
    return "".join(hasil)


# ==================================================================================
# BAGIAN 4: TAHAP 3 - XOR CIPHER
# Teks diubah menjadi byte UTF-8, lalu setiap byte di-XOR dengan byte kunci
# yang diulang secara siklik (cyclic key).
# ==================================================================================

def xor_bytes(data: bytes, key: str) -> bytes:
    """Meng-XOR setiap byte data dengan byte kunci (siklik). XOR bersifat simetris,
    sehingga fungsi ini dipakai baik untuk enkripsi maupun dekripsi XOR."""
    if not key:
        raise ValueError("Kunci XOR tidak boleh kosong.")
    key_bytes = key.encode("utf-8")
    hasil = bytearray(len(data))
    for i, b in enumerate(data):
        hasil[i] = b ^ key_bytes[i % len(key_bytes)]
    return bytes(hasil)


# ==================================================================================
# BAGIAN 5: TAHAP 4 - RSA CIPHER
# Setiap nilai byte (0-255) dienkripsi/didekripsi satu per satu menggunakan
# rumus RSA klasik: C = M^e mod n  |  M = C^d mod n
# ==================================================================================

def rsa_encrypt_bytes(data: bytes, e: int, n: int) -> list:
    """Mengenkripsi setiap byte data menjadi list angka ciphertext RSA."""
    return [pow(byte_val, e, n) for byte_val in data]


def rsa_decrypt_numbers(numbers: list, d: int, n: int) -> bytes:
    """Mendekripsi list angka ciphertext RSA kembali menjadi bytes (nilai 0-255)."""
    hasil = bytearray()
    for num in numbers:
        m = pow(num, d, n)
        if m > 255:
            raise ValueError(
                f"Hasil dekripsi RSA menghasilkan nilai byte {m} (>255). "
                "Kemungkinan kunci RSA (n, d) tidak sesuai dengan kunci saat enkripsi."
            )
        hasil.append(m)
    return bytes(hasil)


# ==================================================================================
# BAGIAN 6: FUNGSI GABUNGAN SUPER ENKRIPSI / SUPER DEKRIPSI
# Menjalankan 4 tahap berurutan dan mengembalikan HASIL SETIAP TAHAP agar bisa
# divisualisasikan langkah demi langkah di UI.
# ==================================================================================

def super_encrypt(plaintext: str, caesar_shift: int, vigenere_key: str,
                   xor_key: str, rsa_e: int, rsa_n: int) -> dict:
    """Menjalankan seluruh alur enkripsi dan mengembalikan dict berisi setiap tahap."""
    tahap1_caesar = caesar_encrypt(plaintext, caesar_shift)
    tahap2_vigenere = vigenere_encrypt(tahap1_caesar, vigenere_key)
    bytes_vigenere = tahap2_vigenere.encode("utf-8")
    tahap3_xor = xor_bytes(bytes_vigenere, xor_key)
    tahap4_rsa = rsa_encrypt_bytes(tahap3_xor, rsa_e, rsa_n)

    return {
        "plaintext": plaintext,
        "hasil_caesar": tahap1_caesar,
        "hasil_vigenere": tahap2_vigenere,
        "bytes_xor": tahap3_xor,
        "ciphertext_angka": tahap4_rsa,
        "ciphertext_string": " ".join(str(n) for n in tahap4_rsa),
    }


def super_decrypt(ciphertext_str: str, caesar_shift: int, vigenere_key: str,
                   xor_key: str, rsa_d: int, rsa_n: int) -> dict:
    """Menjalankan seluruh alur dekripsi (urutan terbalik) dan mengembalikan
    dict berisi hasil setiap tahap."""
    # --- Parsing input ciphertext menjadi list integer ---
    potongan = ciphertext_str.split()
    if not potongan:
        raise ValueError("Ciphertext tidak boleh kosong.")

    angka_list = []
    for p in potongan:
        if not p.lstrip("-").isdigit():
            raise ValueError(
                f"Ciphertext mengandung token yang bukan angka: '{p}'. "
                "Pastikan hanya berisi angka integer dipisahkan spasi."
            )
        angka_list.append(int(p))

    # Tahap 1 dekripsi: RSA -> bytes
    bytes_hasil_rsa = rsa_decrypt_numbers(angka_list, rsa_d, rsa_n)

    # Tahap 2 dekripsi: XOR -> bytes teks vigenere asli
    bytes_hasil_xor = xor_bytes(bytes_hasil_rsa, xor_key)
    try:
        teks_setelah_xor = bytes_hasil_xor.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(
            "Gagal decode UTF-8 setelah dekripsi XOR. Kemungkinan kunci XOR, "
            "kunci RSA, atau ciphertext yang dimasukkan tidak tepat."
        ) from exc

    # Tahap 3 dekripsi: Vigenere -> hasil caesar asli
    teks_setelah_vigenere = vigenere_decrypt(teks_setelah_xor, vigenere_key)

    # Tahap 4 dekripsi: Caesar -> plaintext asli
    plaintext_asli = caesar_decrypt(teks_setelah_vigenere, caesar_shift)

    return {
        "angka_list": angka_list,
        "bytes_hasil_rsa": bytes_hasil_rsa,
        "teks_hasil_xor": teks_setelah_xor,
        "teks_hasil_vigenere": teks_setelah_vigenere,
        "plaintext_akhir": plaintext_asli,
    }


# ==================================================================================
# BAGIAN 7: UTILITAS TAMPILAN
# ==================================================================================

def format_bytes_hex(data: bytes) -> str:
    """Menampilkan bytes dalam format hex yang mudah dibaca, contoh: 4A 2F 0B."""
    return " ".join(f"{b:02X}" for b in data)


def format_bytes_dec(data: bytes) -> str:
    """Menampilkan bytes dalam format desimal, contoh: 74 47 11."""
    return " ".join(str(b) for b in data)


PRESET_RSA = {
    "Preset 1 (p=17, q=19)": {"p": 17, "q": 19, "e": 5},
    "Preset 2 (p=13, q=23)": {"p": 13, "q": 23, "e": 5},
    "Preset 3 (p=19, q=23)": {"p": 19, "q": 23, "e": 5},
}


def hitung_kunci_rsa(p: int, q: int, e: int):
    """
    Menghitung n, phi, dan d dari p, q, e.
    Mengembalikan tuple (n, phi, d, list_pesan_error).
    Jika list_pesan_error tidak kosong, berarti kunci tidak valid.
    """
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
        errors.append(
            f"Modulus n = {n} (<= 255). Nilai n harus > 255 agar nilai byte "
            "0-255 tidak rusak/terpotong akibat modulo. Pilih p dan q yang lebih besar."
        )

    if e <= 1 or e >= phi:
        errors.append(f"Nilai e = {e} harus berada di antara 1 dan phi(n) = {phi}.")
    elif gcd(e, phi) != 1:
        errors.append(f"Nilai e = {e} tidak koprima dengan phi(n) = {phi} (gcd != 1).")

    if errors:
        return n, phi, None, errors

    d = mod_inverse(e, phi)
    if d is None:
        errors.append("Gagal menghitung invers modular d. Coba nilai e yang lain.")
        return n, phi, None, errors

    return n, phi, d, []


# ==================================================================================
# BAGIAN 8: APLIKASI STREAMLIT (UI)
# ==================================================================================

st.set_page_config(page_title="Super Enkripsi", page_icon="🔐", layout="wide")

st.title("🔐 Super Enkripsi")
st.caption("Gabungan 4 Algoritma Berlapis: Caesar → Vigenère → XOR → RSA")

st.markdown(
    """
    Aplikasi ini mengenkripsi teks melalui **4 tahap berurutan**:
    `Plaintext → Caesar → Vigenère → XOR (byte) → RSA → Ciphertext (angka)`.
    Proses dekripsi menjalankan urutan **terbalik**:
    `Ciphertext (angka) → RSA → XOR → Vigenère → Caesar → Plaintext`.
    """
)

st.divider()

# ----------------------------------------------------------------------------------
# PENGATURAN KUNCI (dipakai bersama oleh mode Enkripsi & Dekripsi)
# ----------------------------------------------------------------------------------
st.subheader("⚙️ Pengaturan Kunci")

with st.expander("🔑 Kunci Caesar & Vigenère & XOR", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        caesar_shift = st.number_input(
            "Kunci Caesar (shift/integer)",
            min_value=-1000, max_value=1000, value=3, step=1,
            help="Jumlah pergeseran huruf alfabet, misal 3."
        )
    with col2:
        vigenere_key = st.text_input(
            "Kunci Vigenère (teks alfabet)",
            value="KUNCI",
            help="Hanya huruf A-Z/a-z yang dipakai, karakter lain diabaikan."
        )
    with col3:
        xor_key = st.text_input(
            "Kunci XOR (teks bebas)",
            value="SECRET",
            help="Bisa berupa teks bebas, akan diubah ke byte UTF-8."
        )

with st.expander("🔐 Kunci RSA (n, e, d)", expanded=True):
    opsi_rsa = st.radio(
        "Pilih metode penentuan kunci RSA:",
        ["Opsi A: Preset Otomatis", "Opsi B: Manual (p, q, e)"],
        horizontal=True,
    )

    rsa_n, rsa_e, rsa_d, rsa_phi = None, None, None, None
    rsa_valid = False

    if opsi_rsa == "Opsi A: Preset Otomatis":
        nama_preset = st.selectbox("Pilih pasangan prima siap pakai:", list(PRESET_RSA.keys()))
        preset = PRESET_RSA[nama_preset]
        p_val, q_val, e_val = preset["p"], preset["q"], preset["e"]
        rsa_n, rsa_phi, rsa_d, errors = hitung_kunci_rsa(p_val, q_val, e_val)
        rsa_e = e_val

        if errors:
            for err in errors:
                st.error(err)
        else:
            rsa_valid = True
            st.success(
                f"p={p_val}, q={q_val}  →  n={rsa_n}, φ(n)={rsa_phi}, e={rsa_e}, d={rsa_d}"
            )

    else:  # Opsi B: Manual
        colp, colq, cole = st.columns(3)
        with colp:
            p_val = st.number_input("Bilangan prima p", min_value=2, value=17, step=1)
        with colq:
            q_val = st.number_input("Bilangan prima q", min_value=2, value=19, step=1)
        with cole:
            e_val = st.number_input("Kunci publik e", min_value=2, value=5, step=1)

        rsa_n, rsa_phi, rsa_d, errors = hitung_kunci_rsa(int(p_val), int(q_val), int(e_val))
        rsa_e = int(e_val)

        if errors:
            for err in errors:
                st.error(f"⚠️ {err}")
        else:
            rsa_valid = True
            st.success(
                f"Perhitungan berhasil → n = {rsa_n}, φ(n) = {rsa_phi}, "
                f"e = {rsa_e}, d (private key) = {rsa_d}"
            )

st.divider()

# ----------------------------------------------------------------------------------
# MODE OPERASI: ENKRIPSI / DEKRIPSI
# ----------------------------------------------------------------------------------
tab_enkripsi, tab_dekripsi = st.tabs([" Mode Enkripsi", " Mode Dekripsi"])

# ============================== MODE ENKRIPSI ======================================
with tab_enkripsi:
    st.subheader("Mode Enkripsi")
    plaintext_input = st.text_area(
        "Masukkan Plaintext (teks asli):",
        height=150,
        placeholder="Ketik atau tempel teks yang ingin dienkripsi di sini...",
    )

    if st.button("🔒 Enkripsi Sekarang", type="primary", key="btn_enkripsi"):
        # --- Validasi input dasar ---
        if not plaintext_input:
            st.error(" Plaintext tidak boleh kosong.")
        elif not vigenere_key.strip():
            st.error(" Kunci Vigenère tidak boleh kosong.")
        elif not xor_key:
            st.error(" Kunci XOR tidak boleh kosong.")
        elif not rsa_valid:
            st.error(" Kunci RSA belum valid. Perbaiki pengaturan kunci RSA di atas terlebih dahulu.")
        else:
            try:
                hasil = super_encrypt(
                    plaintext_input, int(caesar_shift), vigenere_key, xor_key, rsa_e, rsa_n
                )

                st.success(" Enkripsi berhasil dilakukan!")

                st.markdown("###  Ciphertext Final (deretan angka)")
                st.code(hasil["ciphertext_string"], language="text")

                st.markdown("### 🔍 Visualisasi Proses Bertahap")

                with st.expander("Tahap 1 — Caesar Cipher", expanded=False):
                    st.write(f"**Kunci shift:** {int(caesar_shift)}")
                    st.write("**Teks Asli (Plaintext):**")
                    st.code(hasil["plaintext"], language="text")
                    st.write("**Hasil setelah Caesar:**")
                    st.code(hasil["hasil_caesar"], language="text")

                with st.expander("Tahap 2 — Vigenère Cipher", expanded=False):
                    st.write(f"**Kunci Vigenère:** {vigenere_key}")
                    st.write("**Input (hasil Caesar):**")
                    st.code(hasil["hasil_caesar"], language="text")
                    st.write("**Hasil setelah Vigenère:**")
                    st.code(hasil["hasil_vigenere"], language="text")

                with st.expander("Tahap 3 — XOR Cipher (byte)", expanded=False):
                    st.write(f"**Kunci XOR:** {xor_key}")
                    st.write("**Teks Vigenère diubah ke byte UTF-8, lalu di-XOR:**")
                    st.write("Representasi Hex:")
                    st.code(format_bytes_hex(hasil["bytes_xor"]), language="text")
                    st.write("Representasi Desimal (0-255):")
                    st.code(format_bytes_dec(hasil["bytes_xor"]), language="text")

                with st.expander("Tahap 4 — RSA Cipher", expanded=False):
                    st.write(f"**Kunci publik:** e = {rsa_e}, n = {rsa_n}")
                    st.write("**Rumus:** C = M^e mod n, dihitung untuk setiap byte")
                    st.write("**Ciphertext Final (list angka):**")
                    st.code(hasil["ciphertext_string"], language="text")

            except ValueError as e:
                st.error(f"⚠️ Terjadi kesalahan: {e}")
            except Exception as e:
                st.error(f"⚠️ Terjadi kesalahan tak terduga: {e}")

# ============================== MODE DEKRIPSI ======================================
with tab_dekripsi:
    st.subheader("Mode Dekripsi")
    ciphertext_input = st.text_area(
        "Masukkan Ciphertext (deretan angka dipisahkan spasi):",
        height=150,
        placeholder="Contoh: 187 45 231 98 ...",
    )

    if st.button("🔓 Dekripsi Sekarang", type="primary", key="btn_dekripsi"):
        # --- Validasi input dasar ---
        if not ciphertext_input.strip():
            st.error("⚠️ Ciphertext tidak boleh kosong.")
        elif not vigenere_key.strip():
            st.error("⚠️ Kunci Vigenère tidak boleh kosong.")
        elif not xor_key:
            st.error("⚠️ Kunci XOR tidak boleh kosong.")
        elif not rsa_valid:
            st.error("⚠️ Kunci RSA belum valid. Perbaiki pengaturan kunci RSA di atas terlebih dahulu.")
        else:
            try:
                hasil = super_decrypt(
                    ciphertext_input, int(caesar_shift), vigenere_key, xor_key, rsa_d, rsa_n
                )

                st.success("✅ Dekripsi berhasil dilakukan!")

                st.markdown("### 📜 Plaintext Hasil Dekripsi")
                st.code(hasil["plaintext_akhir"], language="text")

                st.markdown("### 🔍 Visualisasi Proses Bertahap")

                with st.expander("Tahap 1 — Dekripsi RSA", expanded=False):
                    st.write(f"**Kunci privat:** d = {rsa_d}, n = {rsa_n}")
                    st.write("**Rumus:** M = C^d mod n, dihitung untuk setiap angka")
                    st.write("**Ciphertext angka (input):**")
                    st.code(" ".join(str(n) for n in hasil["angka_list"]), language="text")
                    st.write("**Hasil dekripsi RSA (byte, representasi Hex):**")
                    st.code(format_bytes_hex(hasil["bytes_hasil_rsa"]), language="text")
                    st.write("**Hasil dekripsi RSA (byte, representasi Desimal):**")
                    st.code(format_bytes_dec(hasil["bytes_hasil_rsa"]), language="text")

                with st.expander("Tahap 2 — Dekripsi XOR", expanded=False):
                    st.write(f"**Kunci XOR:** {xor_key}")
                    st.write("**Byte di-XOR kembali, lalu decode UTF-8 menjadi string:**")
                    st.code(hasil["teks_hasil_xor"], language="text")

                with st.expander("Tahap 3 — Dekripsi Vigenère", expanded=False):
                    st.write(f"**Kunci Vigenère:** {vigenere_key}")
                    st.write("**Hasil setelah dekripsi Vigenère:**")
                    st.code(hasil["teks_hasil_vigenere"], language="text")

                with st.expander("Tahap 4 — Dekripsi Caesar (Plaintext Asli)", expanded=False):
                    st.write(f"**Kunci shift:** {int(caesar_shift)}")
                    st.write("**Hasil akhir setelah dekripsi Caesar (Plaintext):**")
                    st.code(hasil["plaintext_akhir"], language="text")

            except ValueError as e:
                st.error(f"⚠️ Terjadi kesalahan: {e}")
            except Exception as e:
                st.error(f"⚠️ Terjadi kesalahan tak terduga: {e}")

st.divider()
st.caption("Dibuat dengan Streamlit — Modul Super Enkripsi (Caesar → Vigenère → XOR → RSA)")