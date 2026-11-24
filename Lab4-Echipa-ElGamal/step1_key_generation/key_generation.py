"""Step 1 - ElGamal key generation.

Alice creates a public key and a private key:
    1.1. Generate a large random prime p and a generator g of (Z_p*, ·).
         p is taken as a "safe prime" p = 2q + 1 (q also prime), so the group
         Z_p* has order p - 1 = 2q and checking whether g is a generator only
         needs two tests (see is_generator).
    1.2. Select a random integer a with 2 <= a <= p - 2.
    1.3. Compute g^a mod p.
    1.4. Public key: (p, g, g^a mod p).  Private key: a.
"""

import secrets

# Small primes used to quickly throw away obviously composite candidates
# before running the (more expensive) Miller-Rabin test.
SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]


def is_probable_prime(n, rounds=40):
    """Miller-Rabin primality test.

    Returns False if n is definitely composite, True if n is prime with
    probability at least 1 - 4^(-rounds).
    """
    if n < 2:
        return False
    for sp in SMALL_PRIMES:
        if n % sp == 0:
            return n == sp

    # Write n - 1 = 2^s * d with d odd.
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2          # random base in [2, n - 2]
        y = pow(a, d, n)
        if y == 1 or y == n - 1:
            continue                              # this base says "maybe prime"
        for _ in range(s - 1):
            y = pow(y, 2, n)
            if y == n - 1:
                break                             # reached -1, "maybe prime"
        else:
            return False                          # never reached -1 -> composite
    return True


def generate_safe_prime(bits):
    """Return a prime p with `bits` bits such that q = (p - 1) / 2 is also prime."""
    while True:
        # Random q with bits-1 bits: force the top bit (right size) and the low bit (odd).
        q = secrets.randbits(bits - 1) | (1 << (bits - 2)) | 1
        if not is_probable_prime(q):
            continue
        p = 2 * q + 1
        if is_probable_prime(p):
            return p


def is_generator(g, p):
    """Check whether g generates Z_p* for a safe prime p = 2q + 1.

    The order of g divides p - 1 = 2q, so it is one of 1, 2, q, 2q.
    g is a generator (order 2q) exactly when g^2 != 1 and g^q != 1 (mod p).
    """
    q = (p - 1) // 2
    return pow(g, 2, p) != 1 and pow(g, q, p) != 1


def find_generator(p):
    """Return a random generator g of Z_p*, with 2 <= g <= p - 2."""
    while True:
        g = secrets.randbelow(p - 3) + 2          # random g in [2, p - 2]
        if is_generator(g, p):
            return g


def generate_keys(bits=256):
    """Generate Alice's ElGamal key pair.

    Returns:
        public_key:  tuple (p, g, ga) where p is prime, g a generator, ga = g^a mod p
        private_key: int a, random secret with 2 <= a <= p - 2
    """
    if bits < 8:
        raise ValueError("bits must be at least 8")

    p = generate_safe_prime(bits)                 # 1.1 large random prime p
    g = find_generator(p)                         # 1.1 generator g of Z_p*
    a = secrets.randbelow(p - 3) + 2              # 1.2 random a in [2, p - 2]
    ga = pow(g, a, p)                             # 1.3 g^a mod p

    public_key = (p, g, ga)                       # 1.4 public key
    private_key = a                               # 1.4 private key
    return public_key, private_key
