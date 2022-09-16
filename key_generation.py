import gmpy2
from gmpy2 import mpz
from random import randint
from sympy.ntheory import factorint


def generate_keypair():
    """Returns a dict, containing the public and private keys."""
    output = {}
    
    print("Searching for two primes...")
    while True:
        # Generate two large primes, p and q.
        p = generate_prime()
        q = generate_prime()
        # Check that the product of p and q is coprime with the product of (q-1), (p-1).
        if not check_gcd_condition(p, q):
            continue

        # Calculate n = p * q.
        n = p * q

        # Calculate lambda = lcm(p-1, q-1).
        lambda_n = gmpy2.lcm(p - 1, q - 1)

        # Generate a random integer, g, that is both less than n^2, and coprime to n^2
        n2 = n ** 2

        # Are these checks actually necessary?

        g = randint(0, (n2) - 1)
        if gmpy2.gcd(g, n2) != 1:
            continue

        # Is gcd((g^lambda-1)/n,n) equal to 1?
        if gmpy2.gcd((g**lambda_n - 1) // n, n) != 1:
            continue

        # Is g^lambda - 1 mod n == 1?
        g_lambda_n = gmpy2.powmod(g, lambda_n, n)
        if g_lambda_n != 1:
            continue

        #Calculate mu
        g_lambda_n2 = gmpy2.powmod(g, lambda_n, n2)
        mu = gmpy2.powmod(L(g_lambda_n2, n), -1, n)
        
        print(f"    p: {p}")
        print(f"    q: {q}")
        print(f"    n: {n}")
        print(f"    lambda: {lambda_n}")
        print(f"    g:   {g}")
        print(f"    g^lambda mod n: {g_lambda_n}")
        print(f"    mu: {mu}")
        
        break

    # Build the output
    output["public"] = (int(n), int(g))
    output["private"] = (int(lambda_n), int(mu))

    return output


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
