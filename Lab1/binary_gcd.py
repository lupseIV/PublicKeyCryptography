def binary_gcd(a : int,b : int) -> int:
    """
    Binary GCD (Stein's algorithm): computes gcd(a, b) using only
    parity checks, halving (shift right), subtraction and comparison -
    no division or modulo.

    Rules used:
      1. gcd(a, 0) = a
      2. a, b both even      -> gcd(a, b) = 2 * gcd(a/2, b/2)
      3. only one is even    -> divide that one by 2 (2 is not a common factor)
      4. a, b both odd       -> gcd(a, b) = gcd(|a - b|, min(a, b))
                                (|a - b| is even, so rule 3 applies next)
    """
    # k counts the common factors of 2 removed by rule 2;
    # they are multiplied back at the end as 2^k.
    k = 0
    while b != 0 and a != 0:        # rule 1 is the stop condition
        if a & 1 and b & 1:
            # rule 4: both odd
            a, b = abs(a - b), min(a, b)
        elif b & 1:
            # rule 3: a even, b odd -> drop the factor 2 from a
            a = a // 2
        elif a & 1:
            # rule 3: b even, a odd -> drop the factor 2 from b
            b = b // 2
        else:
            # rule 2: both even -> 2 is a common factor, remember it in k
            k += 1
            a, b = a // 2, b // 2
    # one of them is 0, the other one is the odd part of the gcd;
    # shifting left by k multiplies it by 2^k
    return max(a, b) << k
