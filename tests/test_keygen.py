import logging
from random import randint

from gmpy2 import mpz
import helpers
import pallier_parser
from main import is_homomorphic
import pytest
from sympy.ntheory import factorint

logging.basicConfig(level=logging.DEBUG)


L_tests = [
    ((7, 3), 2),
    ((8, 3), 2),
    ((9, 3), 2),
    ((10, 3), 3),
    ((11, 3), 3),
    ((12, 3), 3),
    ((13, 3), 4),
    ((14, 3), 4),
    ((15, 3), 4),
]


@pytest.mark.parametrize("nums, expected", L_tests)
def test_L(nums, expected):
    """Tests that L() is working as intended."""
    assert helpers.L(nums[0], nums[1]) == expected


def test_prime_generator():
    """Tests that the prime generator is working as intended.

    Checks 100000 generated numbers.
    """
    for _ in range(100000):
        p = helpers.generate_prime(4)
        assert len(factorint(p)) == 1
        assert len(str(int(p))) == 4


# Taken from https://asecuritysite.com/principles_pub/pal_ex
keygen_tests = [
    # Valid inputs, should produce keypairs
    [(13, 17, 4886), {"public": (221, 4886), "private": (48, 159)}],
    [(47, 67, 4787652), {"public": (3149, 4787652), "private": (1518, 206)}],
    [(43, 41, 150), {"public": (1763, 150), "private": (840, 672)}],
    # Invalid inputs, should return None
    # fails because g is not coprime to n^2 (g = {13, 17, 221})
    [(13, 17, 221), None],
    # g is greater than n^2
    [(13, 17, 48842), None],
]


@pytest.mark.parametrize("nums,expected", keygen_tests)
def test_calculate_keypair(nums, expected):
    """Tests that the key generation is working as intended."""
    p, q, g = nums
    assert helpers.calculate_keypair(p, q, g) == expected


encryption_tests = [
    [(5, (mpz(16751089), mpz(93932148945646)), 9097175), 269016111860835],
    [(432, (mpz(80501411), mpz(902514156098306)), 41470621), 4992445291325108],
]


@pytest.mark.parametrize("inputs,expected", encryption_tests)
def test_encryption(inputs, expected):
    """Tests that the encryption is working as intended."""
    message, public_key, init_r = inputs
    assert pallier_parser.encrypt(message, public_key, init_r) == expected


decryption_tests = [
    [({'public': (mpz(18057373), mpz(195062812669755)), 'private': (mpz(3007818), mpz(1771420))}, 129050848160304), 403],
    [({'public': (mpz(38151527), mpz(367791877145174)), 'private': (mpz(19069440), mpz(16335875))}, 504324473855033), 9751]
]

@pytest.mark.parametrize("inputs,expected", decryption_tests)
def test_decryption(inputs, expected):
    """Tests that the decryption is working as intended."""
    keypair, message = inputs
    assert pallier_parser.decrypt(message, keypair["public"], keypair["private"]) == expected


message_tests = [
    1,
    12,
    123,
    1234,
    12345,
    123456,
    # Could go on but it'll take forever on my laptop
]


@pytest.mark.parametrize("message", message_tests)
def test_encrypt_decrypt(message):
    """Tests that the encryption and decryption is working as intended."""
    message_length = len(str(message))
    prime_length = (message_length // 2) + 1
    keypair = pallier_parser.generate_keypair(prime_length=prime_length)
    encrypted = pallier_parser.encrypt(message, keypair["public"])
    decrypted = pallier_parser.decrypt(encrypted, keypair["public"], keypair["private"])
    assert decrypted == message


def test_homomorphism():
    """Tests that the implementation is homomorphic.
    Checks 10 generated message combinations.
    Using primes with 3 digits, messages of up to 6 digits can be encrypted.
    """

    for _ in range(10):
        a = randint(1, 9999)
        b = randint(1, 9999)
        if not is_homomorphic(a, b, prime_length=3) == True:
            print(a, b)
            assert False

