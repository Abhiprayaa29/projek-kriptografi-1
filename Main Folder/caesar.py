import streamlit as st

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
# ANTARMUKA STREAMLIT
# =======================================================================

st.set_page_config(page_title="Caesar Cipher", layout="centered")

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