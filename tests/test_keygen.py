import pytest
import key_generation


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
        assert len(key_generation.factors(p)) == 2