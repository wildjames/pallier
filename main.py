import logging

from helpers import calculate_keypair
from pallier_parser import *

logging.basicConfig(level=logging.DEBUG)


def is_homomorphic():
    """Returns True if the implementation is homomorphic."""
    return False


def execute():
    message = 1
    p = 5
    q = 7
    g = 253
    r = None

    message_length = len(str(message))
    logging.info(f"Message length: {message_length}")

    # keypair = calculate_keypair(p, q, g)
    keypair = generate_keypair(prime_length=4)
    logging.info(f"  Keys:  {keypair}")

    encrypted = encrypt(message, keypair["public"], init_r=r)
    logging.info(f"  Encrypted message: {encrypted}")

    decrypted = decrypt(encrypted, keypair["public"], keypair["private"])
    logging.info(f"  Decrypted message: {decrypted}")

    assert decrypted == message, "Failed! Got a decryption of {} instead of {}".format(
        decrypted, message
    )


if __name__ in "__main__":
    execute()
