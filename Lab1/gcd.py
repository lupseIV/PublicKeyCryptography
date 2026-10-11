def gcd_euclid(el1, el2):
    """
    Euclid's algorithm (remainder version): computes gcd(el1, el2).

    Based on the identity gcd(a, b) = gcd(b, a mod b): every common divisor
    of a and b also divides a mod b = a - q*b, and vice versa, so replacing
    (a, b) with (b, a mod b) does not change the gcd. The numbers shrink at
    every step, and when the second one reaches 0 we use gcd(a, 0) = a.

    Works for natural numbers of arbitrary size, because Python's int has
    no size limit and `%` on big integers is implemented in fast C code.
    """
    while el2 != 0:
        # (a, b) -> (b, a mod b); if el1 < el2 the first step just swaps them
        el1, el2 = el2, el1 % el2
    # el2 == 0, so gcd(el1, 0) = el1
    return el1
