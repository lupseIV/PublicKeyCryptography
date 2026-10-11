def factor_gcd(a :int, b : int):
    """
    GCD via prime factorization: factor both numbers, then multiply every
    prime they have in common, raised to the smaller of its two exponents.
    Example: 360 = 2^3 * 3^2 * 5 and 84 = 2^2 * 3 * 7
             -> gcd = 2^min(3,2) * 3^min(2,1) = 4 * 3 = 12

    Only practical for numbers whose prime factors are not too large,
    because trial division is slow (see get_factors).
    """
    # 0 has no prime factorization; every number divides 0, so gcd(a, 0) = a
    if a == 0 or b == 0:
        return max(a,b)
    a_factors, b_factors = get_factors(a), get_factors(b)
    gcd = 1
    for a_fact in a_factors:
        # exponent of this prime in the gcd = smaller of the two exponents
        # (a prime missing from b has exponent 0 there, so it contributes nothing)
        nr_of_factors = min(b_factors.get(a_fact ,0),a_factors[a_fact])
        while  nr_of_factors != 0:
            # remove the shared prime from b so the second loop skips it
            if a_fact in b_factors:
                b_factors.pop(a_fact)
            nr_of_factors -= 1
            gcd *= a_fact

    # second pass over the primes of b; shared primes were already removed
    # above and the others have exponent 0 in a, so this never changes gcd
    for b_fact in b_factors:
        nr_of_factors = min(a_factors.get(b_fact, 0), b_factors[b_fact])
        while nr_of_factors != 0:
            nr_of_factors -= 1
            gcd *= b_fact

    return gcd


def get_factors(a: int):
    """
    Prime factorization by trial division.
    Returns a dictionary {prime: exponent}, e.g. 360 -> {2: 3, 3: 2, 5: 1}.
    """
    if a == 0:
        return {}
    d = 2
    factors = {}
    # It is enough to try divisors d with d*d <= a: a composite number
    # always has a prime factor <= its square root, so once d*d > a,
    # whatever is left of a is either 1 or a single prime.
    while d * d <= a:
        if a % d == 0:
            # d divides a: divide it out and count it (d stays the same,
            # so the same prime is divided out as many times as possible)
            a //= d
            factors[d] = factors.get(d, 0) + 1
        else:
            d += 1
    # the leftover is a prime; it may be one we already counted
    # (e.g. 8 -> 2*2 in the loop, leftover 2), so add 1 instead of setting 1
    if a > 1:
        factors[a] = factors.get(a, 0) + 1

    return factors
