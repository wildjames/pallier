import logging

from helpers import generate_keypair, calculate_keypair
from pallier_parser import add_homo, decrypt, encrypt, is_homomorphic

logging.basicConfig(level=logging.DEBUG)


def execute():
    message = 1
    p = 5
    q = 7
    g = 253
    r = None

    message_length = len(str(message))
    logging.info(f"Message length: {message_length}")

    keypair = calculate_keypair(p, q, g)
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
