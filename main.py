import logging

from helpers import generate_keypair, calculate_keypair
from pallier_parser import add_homo, decrypt, encrypt, is_homomorphic

logging.basicConfig(level=logging.DEBUG)

if __name__ in "__main__":

    message = 123456
    prime_length = 4

    message_length = len(str(message))
    logging.info(f"Message length: {message_length}")
    
    keypair = generate_keypair(prime_length)
    logging.info(f"  Keys:  {keypair}")
    
    encrypted = encrypt(message, keypair["public"])
    logging.info(f"  Encrypted message: {encrypted}")

    decrypted = decrypt(encrypted, keypair["public"], keypair["private"])
    logging.info(f"  Decrypted message: {decrypted}")

    
    assert decrypted == message, "Failed! Got a decryption of {} instead of {}".format(decrypted, message)
