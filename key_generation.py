import gmpy2
from gmpy2 import mpz


def generate_keypair():
    """Returns a dict, containing the public and private keys."""
    return {"public": None, "private": None}


def factors(n):
    """Returns a set of the prime factors of n."""
    result = set()
    result |= {mpz(1), mpz(n)}

    def all_multiples(result, n, factor):
        z = mpz(n)
        while gmpy2.f_mod(mpz(z), factor) == 0:
            z = gmpy2.divexact(z, factor)
            result |= {mpz(factor), z}
        return result

    result = all_multiples(result, n, 2)
    result = all_multiples(result, n, 3)

    for i in range(1, gmpy2.isqrt(n) + 1, 6):
        i1 = mpz(i) + 1
        i2 = mpz(i) + 5
        div1, mod1 = gmpy2.f_divmod(n, i1)
        div2, mod2 = gmpy2.f_divmod(n, i2)
        if mod1 == 0:
            result |= {i1, div1}
        if mod2 == 0:
            result |= {i2, div2}
    return result


def check_gcd_condition(p, q):
    """Checks that p and q follow the requirement:

    gcd( (p*q), (p-1)*(q-1) ) == 1

    Where "gcd" is the greatest common divisor. In effect, this checks that pq and (p-1)(q-1) are coprime.
    """

    pq_factors = factors(p * q)
    pq_minus_1_factors = factors((p - 1) * (q - 1))

    return len(pq_factors & pq_minus_1_factors) == 1
