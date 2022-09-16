from key_generation import generate_keypair
from pallier_parser import encrypt, decrypt, is_homomorphic, add_homo


if __name__ in "__main__":
    keys = generate_keypair(47, 67, 4787652)

    message = 10

    encrypted = encrypt(message, keys["public"], r=106)

    assert encrypted == 2476138

    print(encrypted)
    print()
    print(keys)