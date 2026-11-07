# Pollard p-1 method
import random
from math import gcd


def sieve(n):
    """Return all primes strictly less than n using the sieve of Eratosthenes."""
    if n < 3:
        return []
    is_prime = [True] * n
    is_prime[0] = False
    is_prime[1] = False
    p = 2
    while p * p < n:
        if is_prime[p]:
            for multiple in range(p * p, n, p):
                is_prime[multiple] = False
        p += 1
    return [i for i in range(n) if is_prime[i]]

def pollard(N, b = 100, a = None):
    PRIMES = sieve(b+1) #initialize all primes less than or equal to the bound
    # initialize base
    if a is None:
        # 1 and N-1 (= -1 mod N) always give a^K = 1, so skip them
        BASE = random.randint(2, N-2)
        print("Random base: " + str(BASE))
    else:
        BASE = a

    # Lucky case: the base already shares a factor with N
    D = gcd(BASE, N)
    if D > 1:
        print("SUCCESS (gcd(a, N)): " + str(D))
        return D

    #compute k as the product of primes to the max power i so that prime^i <= bound
    K = 1
    for p in PRIMES:
        i = 1
        while pow(p, i) <= b:
            i += 1
        K = K * pow(p, i-1)

    #compute BASE ^ K mod N
    BASE = pow(BASE, K, N)

    D = gcd(BASE-1, N)

    if D == 1 or D == N:
        print("FAILURE")
        return None
    else:
        print("SUCCESS: " + str(D))
        return D


# Test inputs: run each with default bound and a random base,
# and check that any factor found really divides N.
# Each N = p * q where p-1 is built only from prime powers <= 100
# and q is a safe prime (q-1 = 2 * big prime), so b = 100 finds p.
TEST_NS = [
    2351 * 1619,                          # 4-digit primes
    282439 * 738539,                      # 6-digit primes
    6864108971 * 9335022143,              # 10-digit primes
    959529067947451 * 616416362396867,    # 15-digit primes
]


def run_tests():
    for N in TEST_NS:
        print("N = " + str(N))
        D = pollard(N)
        if D is not None:
            assert N % D == 0, "D does not divide N"
            print("OK: " + str(N) + " = " + str(D) + " * " + str(N // D))
        print()


if __name__ == "__main__":
    N = input("Enter N (empty = run tests): ")
    if not N:
        run_tests()
        raise SystemExit
    N = int(N)
    BOUND = input("Enter BOUND(100): ")
    A = input("Enter base (random): ")

    # Empty answer -> use the default (100 / random base)
    b = int(BOUND) if BOUND else 100
    a = int(A) if A else None
    pollard(N, b, a)