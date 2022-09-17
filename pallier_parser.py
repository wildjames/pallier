import logging
from random import randint

import gmpy2

from helpers import L


def encrypt(m, public_key, r=None):
    """Encrypts a message using the public key.

    The public key is a tuple of the form (n, g).
    """
    m = gmpy2.mpz(m)

    n = public_key[0]
    g = public_key[1]

    if m > n:
        raise ValueError("message cannot exceed n, {} > {}".format(m, n))

    if r is None:
        r = randint(1, n - 1)
        print(f"  r: {r}")
    r = gmpy2.mpz(r)
    logging.debug(f"    r: {r}")

    cipher_text = ((g**m) * (r**n)) % (n**2)

    return cipher_text


def decrypt(message, public_key, private_key):
    """Decrypts a message using the private key.

    The private key is a tuple of the form (lambda, mu).
    """

    lambda_n = private_key[0]
    mu = private_key[1]

    n = public_key[0]

    n2 = n**2
    if message > n2:
        raise ValueError(
            "ciphertext must be less than n^2 (c: {}, n^2: {})".format(message, n2)
        )

    c_lambda_mod_n2 = gmpy2.powmod(message, lambda_n, n2)
    original_message = (L(c_lambda_mod_n2, n) * mu) % n

    return original_message


def is_homomorphic():
    """Returns True if the implementation is homomorphic."""
    return False


def add_homo(c1, c2):
    """Adds two homomorphic ciphertexts."""
    return None
