import pytest
from gmpy2 import mpz
import key_generation


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
    assert key_generation.L(nums[0], nums[1]) == expected


gcd_tests = [
    [
        # Two primes
        (5, 7),
        True,
    ],
    [
        # One is a multiple of the other
        (5, 10),
        False,
    ],
    [
        # Same number against itself
        (10, 10),
        True,
    ],
]


@pytest.mark.parametrize("nums,expected", gcd_tests)
def test_gcd_condition(nums, expected):
    """Tests that the coprime_checker is working as intended."""
    p, q = nums
    assert key_generation.check_gcd_condition(p, q) == expected


def test_prime_generator():
    """Tests that the prime generator is working as intended.

    Checks 1000 generated numnbers.
    """
    for _ in range(1000):
        p = key_generation.generate_prime()
        assert len(key_generation.factorint(p)) == 1


# Taken from https://asecuritysite.com/principles_pub/pal_ex
keygen_tests = [
    [
        (47, 67, 4787652), {'public': (3149, 4787652), 'private': (1518, 206)}
    ],
    [   
        (43, 41, 150), {'public': (1763, 150), 'private': (840, 672)}
    ],
]

@pytest.mark.parametrize("nums,expected", keygen_tests)
def test_keygen(nums, expected):
    """Tests that the key generation is working as intended."""
    p, q, g = nums
    assert key_generation.generate_keypair(p, q, g) == expected