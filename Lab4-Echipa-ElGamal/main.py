"""ElGamal - runs key generation, encryption and decryption end to end."""

from step1_key_generation.key_generation import generate_keys
from step2_encryption.encryption import encrypt
from step3_decryption.decryption import decrypt


def main():
    # TODO: implement
    #   1. public_key, private_key = generate_keys(bits)
    #   2. ciphertext = encrypt(message, public_key)
    #   3. recovered = decrypt(ciphertext, private_key, public_key)
    #   4. check recovered == message
    pass


if __name__ == "__main__":
    main()
