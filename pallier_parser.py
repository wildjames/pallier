import logging
from random import randint

import gmpy2

from helpers import *


def generate_keypair(prime_length=4):
    """Returns a dict, containing the public and private keys. These will be of the form:

    public  = (n, g)
    private = (lambda_n, mu)

    This is generated based off two coprime numbers, p and q, and a generator, g.
    g must be an integer < n^2, where n = p * q.

    Random values will be generated for p, q, and g.

    Inputs:
    -------
    prime_length: int, optional
        The length of the primes to generate; the max message length can be no longer than (pq), 
        so choose this wisely. Defaults to 4, allowing messages of 8 digits.
    
    Returns:
    --------
    keypair: dict
        A dict containing the public and private keys.
    """

    while True:
        p = generate_prime(prime_length)
        q = generate_prime(prime_length)

        # p and q must be different numbers, or this won't be secure!
        # You could do a quick check to see if n is prime, and get p and q from that.
        if p != q:
            break

    # Generate a random integer, g, that is both less than n^2, and coprime to n^2
    n = p * q
    n2 = n**2
    g = randint(0, (n2) - 1)
    g = mpz(g)

    keypair = calculate_keypair(p, q, g)
    # If this fails, try again
    if keypair is None:
        return generate_keypair(prime_length=prime_length)
    return keypair


def encrypt(m, public_key, init_r=None):
    """Encrypts a message using the public key.

    The public key is a tuple of the form (n, g).
    Note that if r is manually specified, it must satisfy the encryption conditions!

    Inputs:
    -------
    m: int
        The message to encrypt.
    public_key: tuple
        The public key, of the form (n, g).
    init_r: int, optional
        The random value to use for encryption. If not specified, a random value will be generated.

    Returns:
    --------
    encrypted_message: int
        The encrypted message.
    """
    m = gmpy2.mpz(m)

    n = public_key[0]
    g = public_key[1]

    if m > n:
        raise ValueError("message ({m}) cannot exceed n ({n})".format(m, n))

    if init_r is None:
        r = randint(1, n - 1)
    else:
        r = init_r

    r = gmpy2.mpz(r)
    logging.debug(f"    r: {r}")

    cipher_text = ((g**m) * (r**n)) % (n**2)

    if gmpy2.gcd(cipher_text, n**2) != 1:
        if init_r is not None:
            raise ValueError("Given value of r cannot be used to encrypt message.")
        # But if I generated a random r, try again!
        return encrypt(m, public_key)

    return cipher_text


def decrypt(message, public_key, private_key):
    """Decrypts a message using the private key.

    The private key is a tuple of the form (lambda, mu).

    Inputs:
    -------
    message: int
        The message to decrypt.
    public_key: tuple
        The public key, of the form (n, g).
    private_key: tuple
        The private key, of the form (lambda, mu).

    Returns:
    --------
    decrypted_message: int
        The decrypted message.
    """

    lambda_n = private_key[0]
    mu = private_key[1]

    n = public_key[0]

    n2 = n**2

    if gmpy2.gcd(message, n2) != 1:
        raise ValueError("message is not coprime to n^2 and cannot be decrypted.")

    if message > n2:
        raise ValueError(
            "ciphertext must be less than n^2 (c: {}, n^2: {})".format(message, n2)
        )

    c_lambda_mod_n2 = gmpy2.powmod(message, lambda_n, n2)
    original_message = (L(c_lambda_mod_n2, n) * mu) % n

    return original_message


def add_homo(c1, c2, public_key):
    """Adds two homomorphic ciphertexts.
    
    Inputs:
    -------
    c1: int
        The first message to add
    c2: int
        The second message to add
    public_key: tuple
        The public key, of the form (n, g)
    
    Returns:
    --------
    summed_message: int
    """
    n = public_key[0]

    summed_message = (c1 * c2) % (n**2)

    return summed_message
