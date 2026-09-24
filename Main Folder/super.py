def caesar_encrypt(plaintext: str, shift: int):
    ciphertext = ""
    print(f"\n--- PROSES ENKRIPSI (Shift: {shift}) ---")
    
    for char in plaintext:
        if char.isupper():
            # A-Z: ASCII 65-90
            orig_idx = ord(char) - ord('A')
            new_idx = (orig_idx + shift) % 26
            new_char = chr(new_idx + ord('A'))
            ciphertext += new_char
            print(f"'{char}' ({orig_idx}) -> ({orig_idx} + {shift}) % 26 = {new_idx} -> '{new_char}'")
        elif char.islower():
            # a-z: ASCII 97-122
            orig_idx = ord(char) - ord('a')
            new_idx = (orig_idx + shift) % 26
            new_char = chr(new_idx + ord('a'))
            ciphertext += new_char
            print(f"'{char}' ({orig_idx}) -> ({orig_idx} + {shift}) % 26 = {new_idx} -> '{new_char}'")
        else:
            # Karakter selain huruf (spasi, angka, tanda baca) dipertahankan
            ciphertext += char
            print(f"'{char}' (non-alfabet) -> tetap '{char}'")
            
    return ciphertext


def caesar_decrypt(ciphertext: str, shift: int):
    plaintext = ""
    print(f"\n--- PROSES DEKRIPSI (Shift: {shift}) ---")
    
    for char in ciphertext:
        if char.isupper():
            cipher_idx = ord(char) - ord('A')
            orig_idx = (cipher_idx - shift) % 26
            orig_char = chr(orig_idx + ord('A'))
            plaintext += orig_char
            print(f"'{char}' ({cipher_idx}) -> ({cipher_idx} - {shift}) % 26 = {orig_idx} -> '{orig_char}'")
        elif char.islower():
            cipher_idx = ord(char) - ord('a')
            orig_idx = (cipher_idx - shift) % 26
            orig_char = chr(orig_idx + ord('a'))
            plaintext += orig_char
            print(f"'{char}' ({cipher_idx}) -> ({cipher_idx} - {shift}) % 26 = {orig_idx} -> '{orig_char}'")
        else:
            plaintext += char
            print(f"'{char}' (non-alfabet) -> tetap '{char}'")
            
    return plaintext



if __name__ == "__main__":
    teks_asli = "Kripto Modern 2026!"
    kunci_geser = 3

    print(f"Plaintext Awal: {teks_asli}")
    
    # 1. Enkripsi
    teks_enkripsi = caesar_encrypt(teks_asli, kunci_geser)
    print(f"\nHasil Enkripsi : {teks_enkripsi}")

    # 2. Dekripsi
    teks_dekripsi = caesar_decrypt(teks_enkripsi, kunci_geser)
    print(f"\nHasil Dekripsi : {teks_dekripsi}")