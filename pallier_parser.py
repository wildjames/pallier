import logging
from random import randint

import gmpy2

from helpers import L


def encrypt(m, public_key, r=None):
    """Encrypts a message using the public key.
    
    The public key is a tuple of the form (n, g).
    """
    n = public_key[0]
    g = public_key[1]

    if m > n:
        raise ValueError("message cannot exceed n, {} > {}".format(m, n))

    if r is None:
        r = randint(0, n)
    logging.debug(f"    r: {r}")

    cipher_text = (g ** m) * (r ** n)
    cipher_text = cipher_text % (n ** 2)

    return cipher_text


def decrypt(c, public_key, private_key):
    """Decrypts a message using the private key.
    
    The private key is a tuple of the form (lambda, mu).
    """

    lambda_n = private_key[0]
    mu = private_key[1]
    n = public_key[0]

    c_lambda_mod_n2 = gmpy2.powmod(c, lambda_n, n**2)
    message = L(c_lambda_mod_n2, n) * mu % n

    return message


def is_homomorphic():
    """Returns True if the implementation is homomorphic."""
    return False


def add_homo(c1, c2):
    """Adds two homomorphic ciphertexts."""
    return None
