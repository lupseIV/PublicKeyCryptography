"""ElGamal - runs key generation, encryption and decryption end to end."""

from step1_key_generation.key_generation import generate_keys
from step2_encryption.encryption import ALPHABET, encrypt_plaintext, validate_plaintext
from step3_decryption.decryption import decrypt

KEY_BITS = 64


def read_plaintext():
    """Ask for a plaintext until a valid one is entered."""
    while True:
        plaintext = input("Plaintext (blanks and letters A-Z only): ")
        try:
            return validate_plaintext(plaintext)
        except ValueError as error:
            print(f"Invalid plaintext: {error}")


def main():
    # 1. Key generation
    public_key, private_key = generate_keys(KEY_BITS)
    p, g, h = public_key
    print(f"Public key:  p = {p}, g = {g}, h = {h}")
    print(f"Private key: x = {private_key}")

    # 2. Encryption
    plaintext = read_plaintext()
    ciphertext = encrypt_plaintext(plaintext, public_key)
    print("Ciphertext:", ciphertext)

    # 3. Decryption, one (c1, c2) pair per character
    recovered = "".join(ALPHABET[decrypt(pair, private_key, public_key)] for pair in ciphertext)
    print("Decrypted: ", recovered)

    # 4. Check
    if recovered == plaintext:
        print("OK: decrypted text matches the plaintext.")
    else:
        print("ERROR: decrypted text does not match the plaintext.")


if __name__ == "__main__":
    main()
