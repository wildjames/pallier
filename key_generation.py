import gmpy2
from gmpy2 import mpz
from random import randint
from sympy.ntheory import factorint


def generate_keypair():
    """Returns a dict, containing the public and private keys."""

    print("Searching for two primes...")
    i = 0
    while True:
        # Generate two large primes, p and q.
        p = generate_prime()
        q = generate_prime()
        # Check that the product of p and q is coprime with the product of (q-1), (p-1).
        if check_gcd_condition(p, q):
            break
        print(f"  {i}", end="\r")
        i += 1
    print("\nFound two primes that satisfy the condition:")
    print(f"    p: {p}")
    print(f"    q: {q}")

    # Calculate n = p * q.
    n = p * q
    print(f"    n: {n}")

    # Calculate lambda(n) = lcm(p-1, q-1).
    lambda_n = gmpy2.lcm(p - 1, q - 1)
    print(f"    lambda(n): {lambda_n}")

    # Generate a random integer, g, that is both less than n^2, and coprime to n^2
    n_factors = list(factorint(n**2).keys())
    print(f"n^2: {n**2}")
    print(f"n^2 has factors: {n_factors}")
    while True:
        g = randint(0, (n**2) - 1)
        print(factorint(g).keys())
        common_factors = [k for k in factorint(g).keys() if k in n_factors]
        print(f"Common factors: {common_factors}")
        input("> ")

        if len(common_factors) != 0:
            continue
        print(f"Found g = {g}")

        # Calculate mu = (lambda(n) ^ -1) mod n.
        g_lambda_n = gmpy2.powmod(g, lambda_n, n**2)
        tmp = pow(L(g_lambda_n, n), -1)
        mu = tmp % n

        if mu != 0:
            print(f"    mu: {mu}")
            break
        print("Mu does not exist")

    # Calculate the public key, e, such that 1 < e < lambda(n) and gcd(e, lambda(n)) == 1.

    # Calculate the private key, d, such that d * e == 1 (mod lambda(n)).

    # Return the public and private keys.

    return {"public": None, "private": None}


def L(x, n):
    """Returns the the minimum value of v such that (x-1) > v*n."""
    return (x - 1) // n


def check_gcd_condition(p, q):
    """Checks that p and q follow the requirement:

    gcd( (p*q), (p-1)*(q-1) ) == 1

    Where "gcd" is the greatest common divisor. In effect, this checks that pq and (p-1)(q-1) are coprime.
    """
    return gmpy2.gcd(p * q, (p - 1) * (q - 1)) == 1


def generate_prime():
    """Returns a prime number between 1,000,000 and 10,000,000."""
    random_starter = randint(int(1e3), int(1e4))

    return gmpy2.next_prime(random_starter)
