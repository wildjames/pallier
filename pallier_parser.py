from random import randint
import numpy as np


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
    print(f"    r: {r}")

    cipher_text = (g ** m) * (r ** n)
    cipher_text = cipher_text % (n ** 2)

    return cipher_text


def decrypt(c, private_key):
    """Decrypts a message using the private key.
    
    The private key is a tuple of the form (lambda, mu).
    """
    return None


def is_homomorphic():
    """Returns True if the implementation is homomorphic."""
    return False


def add_homo(c1, c2):
    """Adds two homomorphic ciphertexts."""
    return None
