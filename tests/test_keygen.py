import logging

import helpers
import pallier_parser
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
    [(13, 17, 4886), {"public": (221, 4886), "private": (48, 159)}],
    [(47, 67, 4787652), {"public": (3149, 4787652), "private": (1518, 206)}],
    [(43, 41, 150), {"public": (1763, 150), "private": (840, 672)}],
]


@pytest.mark.parametrize("nums,expected", keygen_tests)
def test_calculate_keypair(nums, expected):
    """Tests that the key generation is working as intended."""
    p, q, g = nums
    assert helpers.calculate_keypair(p, q, g) == expected


message_tests = [
    1,
    12,
    123,
    1234,
    12345,
    # 123456,
    # 1234567,
]


@pytest.mark.parametrize("message", message_tests)
def test_encrypt_decrypt(message):
    """Tests that the encryption and decryption is working as intended."""
    message_length = len(str(message))
    prime_length = (message_length // 2) + 1
    keypair = helpers.generate_keypair(prime_length=prime_length)
    encrypted = pallier_parser.encrypt(message, keypair["public"])
    decrypted = pallier_parser.decrypt(encrypted, keypair["public"], keypair["private"])
    assert decrypted == message
