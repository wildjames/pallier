import logging
from calendar import c
from random import randint

import gmpy2
from gmpy2 import mpz

logging.basicConfig(level=logging.DEBUG)


def calculate_keypair(p, q, g):
    """Returns a dict, containing the public and private keys. These will be of the form:

    public  = (n, g)
    private = (lambda_n, mu)

    This is generated based off two coprime numbers, p and q, and a generator, g.
    g must be an integer < n^2, where n = p * q.
    """
    # Just make sure they're mpz objects
    p = mpz(p)
    q = mpz(q)

    # Check that the product of p and q is coprime with the product of (q-1), (p-1).
    if not gmpy2.gcd(p * q, ((p - 1) * (q - 1))) == 1:
        logging.debug("p and q are not coprime with (p-1)(q-1)")
        return

    n = p * q

    # Calculate lambda = lcm(p-1, q-1).
    lambda_n = gmpy2.lcm(p - 1, q - 1)

    # Generate a random integer, g, that is both less than n^2, and coprime to n^2
    n2 = n**2
    if not g < n2:
        raise ValueError("g must be less than (p*q)^2")
    g = mpz(g)

    if gmpy2.gcd(g, n2) != 1:
        logging.debug(f"    g = {g} is not coprime to n^2 = {n2}")
        return

    # Are these checks actually necessary? You get them for free if p and q have the same length, I think.
    # Is gcd((g^lambda-1)/n,n) equal to 1?
    if gmpy2.gcd((g**lambda_n - 1) // n, n) != 1:
        logging.debug(f"    (g^lambda-1)/n is not coprime to n = {n}")
        return

    # # Is g^lambda - 1 mod n == 1?
    g_lambda_n = gmpy2.powmod(g, lambda_n, n)
    if g_lambda_n != 1:
        logging.debug(f"    g^lambda-1 = {g_lambda_n} is not equal to 1")
        return

    # Calculate mu
    g_lambda_n2 = gmpy2.powmod(g, lambda_n, n2)
    mu_tmp = L(g_lambda_n2, n)
    mu = gmpy2.powmod(mu_tmp, -1, n)

    logging.debug(f"    p: {p}")
    logging.debug(f"    q: {q}")
    logging.debug(f"    n: {n}")
    logging.debug(f"    lambda: {lambda_n}")
    logging.debug(f"    g:   {g}")
    logging.debug(f"    g^lambda mod n: {g_lambda_n}")
    logging.debug(f"    L(g^lambda mod n^2): {L(g_lambda_n2, n)}")
    logging.debug(f"    mu: {mu}")

    # Build the output
    output = {"public": (n, g), "private": (lambda_n, mu)}

    return output


def L(x, n):
    """Returns the the minimum value of v such that (x-1) > v*n."""
    return (x - 1) // n


def generate_prime(n_digits=4):
    """Returns a prime number of the specified length."""
    lo = int(10 ** (n_digits - 1))
    hi = int(10**n_digits)

    r = randint(lo, hi)
    number = gmpy2.next_prime(r)

    # If the generated number is too high, try again.
    # This can happen if, for example for n_digits = 2, you might generate r = 99.
    # The next prime will be 101 which has too many digits
    if number > hi:
        return generate_prime(n_digits=n_digits)

    return number
