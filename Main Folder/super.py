def process_caesar(text: str, shift: int, mode: str = "enkripsi"):
    result = ""
    # Jika dekripsi, balik arah pergeseran (shift menjadi negatif)
    s = shift if mode == "enkripsi" else -shift

    print(f"\n--- PROSES {mode.upper()} ---")
    for char in text:
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            # Hitung pergeseran alfabet (0 - 25)
            orig_idx = ord(char) - base
            new_idx = (orig_idx + s) % 26
            new_char = chr(new_idx + base)

            print(f"'{char}' -> index ({orig_idx} {'+' if s >= 0 else '-'} {abs(s)}) % 26 = {new_idx} -> '{new_char}'")
            result += new_char
        else:
            print(f"'{char}' -> bukan huruf (tetap)")
            result += char

    return result


if __name__ == "__main__":
    plaintext = input("Masukkan plaintext : ")
    kunci = int(input("Masukkan shift (angka): "))

    # Enkripsi
    ciphertext = process_caesar(plaintext, kunci, mode="enkripsi")
    print(f"\nHasil Enkripsi: {ciphertext}")

    # Dekripsi
    decrypted_text = process_caesar(ciphertext, kunci, mode="dekripsi")
    print(f"\nHasil Dekripsi: {decrypted_text}")