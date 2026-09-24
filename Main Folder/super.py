# ==========================================
# 1. ALGORITMA DASAR
# ==========================================
def caesar_cipher(text: str, shift: int, mode: str = "enkripsi") -> str:
    result = ""
    s = shift if mode == "enkripsi" else -shift

    print(f"\n[Detail Proses Caesar ({mode.upper()})]")
    for char in text:
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            orig_idx = ord(char) - base
            new_idx = (orig_idx + s) % 26
            new_char = chr(new_idx + base)
            print(f"'{char}' ({orig_idx}) -> ({orig_idx} {'+' if s >= 0 else '-'} {abs(s)}) % 26 = {new_idx} -> '{new_char}'")
            result += new_char
        else:
            print(f"'{char}' (non-huruf tetap)")
            result += char
    return result


def rc4_crypt(data: bytes, key: str) -> bytes:
    key_bytes = key.encode("utf-8")
    s_box = list(range(256))
    j = 0

    # KSA
    for i in range(256):
        j = (j + s_box[i] + key_bytes[i % len(key_bytes)]) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]

    # PRGA & XOR
    i = 0
    j = 0
    out = []
    print("\n[Detail Proses RC4 (Byte XOR)]")
    for idx, byte in enumerate(data):
        i = (i + 1) % 256
        j = (j + s_box[i]) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]

        k = s_box[(s_box[i] + s_box[j]) % 256]
        res_byte = byte ^ k
        out.append(res_byte)
        print(f"Byte ke-{idx+1}: {byte:#04x} ^ Keystream {k:#04x} = {res_byte:#04x}")

    return bytes(out)


# ==========================================
# 2. LOGIKA GABUNGAN (SUPER ENKRIPSI)
# ==========================================
def combined_encrypt(plaintext: str, caesar_key: int, rc4_key: str) -> str:
    print("\n>>> TAHAP 1: CAESAR CIPHER <<<")
    caesar_res = caesar_cipher(plaintext, caesar_key, mode="enkripsi")
    print(f"Hasil Tahap 1 (Caesar): {caesar_res}")

    print("\n>>> TAHAP 2: RC4 STREAM CIPHER <<<")
    rc4_bytes = rc4_crypt(caesar_res.encode("utf-8"), rc4_key)
    hex_output = rc4_bytes.hex()
    print(f"Hasil Tahap 2 (Hex)   : {hex_output}")

    return hex_output


def combined_decrypt(ciphertext_hex: str, caesar_key: int, rc4_key: str) -> str:
    print("\n>>> TAHAP 1: DEKRIPSI RC4 (HEX TO BYTE) <<<")
    cipher_bytes = bytes.fromhex(ciphertext_hex)
    decrypted_bytes = rc4_crypt(cipher_bytes, rc4_key)
    caesar_text = decrypted_bytes.decode("utf-8")
    print(f"Hasil Tahap 1 (Teks Caesar): {caesar_text}")

    print("\n>>> TAHAP 2: DEKRIPSI CAESAR CIPHER <<<")
    original_text = caesar_cipher(caesar_text, caesar_key, mode="dekripsi")
    print(f"Hasil Tahap 2 (Plaintext)  : {original_text}")

    return original_text


# ==========================================
# 3. SISTEM MENU INTERAKTIF
# ==========================================
def menu():
    while True:
        print("\n" + "=" * 40)
        print("     APLIKASI KRIPTOGRAFI SEDERHANA")
        print("=" * 40)
        print("1. Enkripsi")
        print("2. Dekripsi")
        print("3. Keluar")
        opsi_operasi = input("Pilih operasi (1/2/3): ").strip()

        if opsi_operasi == "3":
            print("Program selesai.")
            break
        elif opsi_operasi not in ["1", "2"]:
            print("Pilihan tidak valid, coba lagi.")
            continue

        print("\n--- PILIH ALGORITMA ---")
        print("1. Caesar Cipher (Klasik)")
        print("2. RC4 (Modern)")
        print("3. Super Enkripsi (Caesar + RC4)")
        opsi_metode = input("Pilih metode (1/2/3): ").strip()

        try:
            # === ALUR ENKRIPSI ===
            if opsi_operasi == "1":
                plaintext = input("\nMasukkan teks (plaintext): ")

                if opsi_metode == "1":
                    shift = int(input("Masukkan shift Caesar (angka): "))
                    hasil = caesar_cipher(plaintext, shift, mode="enkripsi")
                    print(f"\n[HASIL ENKRIPSI CAESAR]: {hasil}")

                elif opsi_metode == "2":
                    key = input("Masukkan kunci RC4 (teks): ")
                    data_bytes = plaintext.encode("utf-8")
                    hasil_bytes = rc4_crypt(data_bytes, key)
                    print(f"\n[HASIL ENKRIPSI RC4 (Hex)]: {hasil_bytes.hex()}")

                elif opsi_metode == "3":
                    shift = int(input("Masukkan shift Caesar (angka): "))
                    key = input("Masukkan kunci RC4 (teks): ")
                    hasil = combined_encrypt(plaintext, shift, key)
                    print(f"\n[HASIL SUPER ENKRIPSI (Hex)]: {hasil}")
                else:
                    print("Pilihan algoritma tidak dikenali.")

            # === ALUR DEKRIPSI ===
            elif opsi_operasi == "2":
                ciphertext = input("\nMasukkan teks sandi (ciphertext): ")

                if opsi_metode == "1":
                    shift = int(input("Masukkan shift Caesar (angka): "))
                    hasil = caesar_cipher(ciphertext, shift, mode="dekripsi")
                    print(f"\n[HASIL DEKRIPSI CAESAR]: {hasil}")

                elif opsi_metode == "2":
                    key = input("Masukkan kunci RC4 (teks): ")
                    cipher_bytes = bytes.fromhex(ciphertext)
                    hasil_bytes = rc4_crypt(cipher_bytes, key)
                    print(f"\n[HASIL DEKRIPSI RC4]: {hasil_bytes.decode('utf-8')}")

                elif opsi_metode == "3":
                    shift = int(input("Masukkan shift Caesar (angka): "))
                    key = input("Masukkan kunci RC4 (teks): ")
                    hasil = combined_decrypt(ciphertext, shift, key)
                    print(f"\n[HASIL DEKRIPSI SUPER ENKRIPSI]: {hasil}")
                else:
                    print("Pilihan algoritma tidak dikenali.")

        except ValueError as err:
            print(f"\n[Error Input]: Pastikan format data dan kunci sesuai ({err}).")
        except Exception as err:
            print(f"\n[Error Operasi]: Terjadi kesalahan saat memproses ({err}).")


if __name__ == "__main__":
    menu()