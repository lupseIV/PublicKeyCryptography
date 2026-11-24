"""Step 3 - ElGamal decryption.

Alice decrypts the message from Bob:
    3.1. Use the private key a to get the message  m = alpha^(-a) * beta mod p.

Why it works: Bob sent alpha = g^k and beta = m * (g^a)^k, so
    alpha^(-a) * beta = g^(-k*a) * m * g^(a*k) = m   (mod p).
"""


def decrypt(ciphertext, private_key, public_key):
    """Decrypt ciphertext (alpha, beta) using private key a and public key (p, g, ga).

    Returns:
        m: int, recovered as alpha^(-a) * beta mod p
    """
    alpha, beta = ciphertext
    a = private_key
    p = public_key[0]                             # only p is needed from the public key

    if not (0 < alpha < p and 0 <= beta < p):
        raise ValueError("ciphertext values must be in the range [0, p)")

    # pow with a negative exponent computes the modular inverse: (alpha^a)^(-1) mod p
    m = (pow(alpha, -a, p) * beta) % p            # 3.1 m = alpha^(-a) * beta mod p
    return m
