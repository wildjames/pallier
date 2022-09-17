import logging

from helpers import generate_keypair, calculate_keypair
from pallier_parser import add_homo, decrypt, encrypt, is_homomorphic

logging.basicConfig(level=logging.DEBUG)


def execute():
    message = 1
    prime_length = 2

    message_length = len(str(message))
    logging.info(f"Message length: {message_length}")

    # keypair = generate_keypair(prime_length)
    # keypair = calculate_keypair(67, 37, 3903017)
    keypair = calculate_keypair(5, 7, 253)
    logging.info(f"  Keys:  {keypair}")

    encrypted = encrypt(message, keypair["public"], 10)
    logging.info(f"  Encrypted message: {encrypted}")

    decrypted = decrypt(encrypted, keypair["public"], keypair["private"])
    logging.info(f"  Decrypted message: {decrypted}")

    assert decrypted == message, "Failed! Got a decryption of {} instead of {}".format(
        decrypted, message
    )


if __name__ in "__main__":
    execute()
