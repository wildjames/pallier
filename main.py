import logging

from helpers import calculate_keypair
from pallier_parser import *

logging.basicConfig(level=logging.DEBUG)


def is_homomorphic(message_a, message_b, prime_length=4):
    """Returns True if the implementation is homomorphic."""

    keypair = generate_keypair(prime_length)

    encrypted_a = encrypt(message_a, keypair["public"])
    encrypted_b = encrypt(message_b, keypair["public"])

    encrypted_sum = add_homo(encrypted_a, encrypted_b, keypair["public"])

    decrypted_sum = decrypt(encrypted_sum, keypair["public"], keypair["private"])

    logging.debug("Checking for homomorphism in the implementation.")
    logging.debug(f"Message A: {message_a}")
    logging.debug(f"Message B: {message_b}")
    logging.debug(f"Sum: {message_a + message_b}")
    logging.debug(f"Decrypted sum: {decrypted_sum}")

    return decrypted_sum == (message_a + message_b)


def execute():
    message = 593

    message_length = len(str(message))
    logging.info(f"Message length: {message_length}")

    # keypair = calculate_keypair(p, q, g)
    keypair = generate_keypair(prime_length=4)
    logging.info(f"  Keys:  {keypair}")

    encrypted = encrypt(message, keypair["public"], init_r=None)
    logging.info(f"  Encrypted message: {encrypted}")

    decrypted = decrypt(encrypted, keypair["public"], keypair["private"])
    logging.info(f"  Decrypted message: {decrypted}")

    assert decrypted == message, "Failed! Got a decryption of {} instead of {}".format(
        decrypted, message
    )


if __name__ == "__main__":
    execute()

    print("\n\n")

    result = is_homomorphic(2, 6)

    print("\n\nHomomorphic? {}".format(result))
