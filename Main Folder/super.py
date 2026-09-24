# ==========================================
# 1. ALGORITMA CAESAR CIPHER (KLASIK)
# ==========================================
def caesar_cipher(text: str, shift: int, mode: str = "enkripsi") -> str:
    result = ""
    s = shift if mode == "enkripsi" else -shift

    for char in text:
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            orig_idx = ord(char) - base
            new_idx = (orig_idx + s) % 26
            result += chr(new_idx + base)
        else:
            result += char
    return result


# ==========================================
# 2. ALGORITMA RC4 (MODERN - STREAM CIPHER)
# ==========================================
def rc4_crypt(data: bytes, key: str) -> bytes:
    # --- KSA (Key-Scheduling Algorithm) ---
    key_bytes = key.encode("utf-8")
    s_box = list(range(256))
    j = 0

    for i in range(256):
        j = (j + s_box[i] + key_bytes[i % len(key_bytes)]) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]

    # --- PRGA (Pseudo-Random Generation Algorithm) & XOR ---
    i = 0
    j = 0
    out = []

    for byte in data:
        i = (i + 1) % 256
        j = (j + s_box[i]) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]

        k = s_box[(s_box[i] + s_box[j]) % 256]
        out.append(byte ^ k)  # Operasi XOR

    return bytes(out)


# ==========================================
# 3. PENGGABUNGAN (SUPER ENKRIPSI SEDERHANA)
# ==========================================
def combined_encrypt(plaintext: str, caesar_key: int, rc4_key: str):
    print("\n" + "=" * 45)
    print("           PROSES ENKRIPSI GABUNGAN")
    print("=" * 45)
    print(f"Plaintext Awal        : {plaintext}")

    # Tahap 1: Caesar Cipher
    caesar_result = caesar_cipher(plaintext, caesar_key, mode="enkripsi")
    print(f"[1] Hasil Caesar      : {caesar_result}")

    # Tahap 2: Konversi string ke byte UTF-8
    raw_bytes = caesar_result.encode("utf-8")

    # Tahap 3: RC4 Stream Cipher
    rc4_bytes = rc4_crypt(raw_bytes, rc4_key)

    # Tahap 4: Hex Encoding (agar karakter aman dicetak)
    hex_output = rc4_bytes.hex()
    print(f"[2] Hasil RC4 (Hex)   : {hex_output}")

    return hex_output


def combined_decrypt(ciphertext_hex: str, caesar_key: int, rc4_key: str):
    print("\n" + "=" * 45)
    print("           PROSES DEKRIPSI GABUNGAN")
    print("=" * 45)
    print(f"Ciphertext Hex        : {ciphertext_hex}")

    # Tahap 1: Hex Decoding ke byte biner
    cipher_bytes = bytes.fromhex(ciphertext_hex)

    # Tahap 2: Dekripsi RC4 (XOR ulang dengan keystream yang sama)
    decrypted_bytes = rc4_crypt(cipher_bytes, rc4_key)
    caesar_text = decrypted_bytes.decode("utf-8")
    print(f"[1] Hasil Dekripsi RC4: {caesar_text}")

    # Tahap 3: Dekripsi Caesar Cipher (geser mundur)
    original_text = caesar_cipher(caesar_text, caesar_key, mode="dekripsi")
    print(f"[2] Hasil Plaintext   : {original_text}")

    return original_text


# ==========================================
# 4. EKSEKUSI UTAMA
# ==========================================
if __name__ == "__main__":
    teks = input("Masukkan plaintext          : ")
    kunci_caesar = int(input("Masukkan shift Caesar (angka): "))
    kunci_rc4 = input("Masukkan kunci RC4 (teks)   : ")

    # Jalankan Enkripsi
    cipher_final = combined_encrypt(teks, kunci_caesar, kunci_rc4)

    # Jalankan Dekripsi
    teks_pulih = combined_decrypt(cipher_final, kunci_caesar, kunci_rc4)