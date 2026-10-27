def sieve(n):
    """Return all primes strictly less than n using the sieve of Eratosthenes."""
    if n < 3:
        return []

    # is_prime[i] is True while i is still considered prime.
    # The list covers 0 .. n-1, so only numbers less than n are handled.
    is_prime = [True] * n
    is_prime[0] = False
    is_prime[1] = False

    p = 2
    # Marking can stop once p*p reaches n: every composite below n
    # has a prime factor p with p*p < n, so nothing is left to cross out.
    while p * p < n:
        if is_prime[p]:
            # Multiples of p below p*p have a smaller prime factor,
            # so they were already crossed out; start at p*p.
            for multiple in range(p * p, n, p):
                is_prime[multiple] = False
        p += 1

    # Every index still True was never crossed out, so it is prime.
    return [i for i in range(n) if is_prime[i]]


if __name__ == "__main__":
    bound = int(input("Enter the bound n: "))
    print(sieve(50))
    print(sieve(100))
    print(sieve(200))
    print(sieve(300))
    print(sieve(1000))
    print(sieve(bound))
