"""Step 2 - ElGamal encryption."""

import secrets

# Setting: 27-character alphabet, blank = 0, A = 1, ..., Z = 26.
ALPHABET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def validate_public_key(public_key):
    """Check that public_key is a tuple (p, g, h) usable with the 27-letter alphabet."""
    if not isinstance(public_key, (tuple, list)) or len(public_key) != 3:
        raise ValueError("Public key must be a tuple (p, g, h).")
    p, g, h = public_key
    if not all(isinstance(v, int) and not isinstance(v, bool) for v in (p, g, h)):
        raise ValueError("Public key values p, g, h must be integers.")
    if p <= len(ALPHABET):
        raise ValueError(f"p must be greater than {len(ALPHABET)} to encode every character.")
    if not 1 < g < p:
        raise ValueError("g must satisfy 1 < g < p.")
    if not 1 <= h < p:
        raise ValueError("h must satisfy 1 <= h < p.")


def validate_plaintext(plaintext):
    """Validate the plaintext and return it in upper case.

    The plaintext must be a non-empty string made only of blanks and English letters.
    """
    if not isinstance(plaintext, str):
        raise ValueError("Plaintext must be a string.")
    if not plaintext:
        raise ValueError("Plaintext must not be empty.")
    normalized = plaintext.upper()
    for position, char in enumerate(normalized):
        if char not in ALPHABET:
            raise ValueError(
                f"Invalid character {plaintext[position]!r} at position {position}: "
                "only blanks and the letters A-Z are allowed."
            )
    return normalized


def encrypt(message, public_key):
    """Encrypt an integer message (0 <= message < p) with public_key (p, g, h).

    Returns:
        ciphertext: tuple (c1, c2) where c1 = g^k mod p, c2 = message * h^k mod p
    """
    p, g, h = public_key
    if not isinstance(message, int) or not 0 <= message < p:
        raise ValueError("Message must be an integer with 0 <= message < p.")
    k = secrets.randbelow(p - 2) + 1  # fresh random ephemeral key, 1 <= k <= p - 2
    c1 = pow(g, k, p)
    c2 = (message * pow(h, k, p)) % p
    return c1, c2


def encrypt_plaintext(plaintext, public_key):
    """Validate and encrypt a text over the 27-character alphabet.

    Each character is mapped to its alphabet index and encrypted separately
    with its own random k.

    Returns:
        list of (c1, c2) pairs, one per character
    """
    validate_public_key(public_key)
    normalized = validate_plaintext(plaintext)
    return [encrypt(ALPHABET.index(char), public_key) for char in normalized]
