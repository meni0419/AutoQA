"""
Протестируйте is_even и is_odd для чисел: 0, 1, 2, -1, -2.
"""
import pytest
from evenOddChecker import EvenOddChecker

@pytest.fixture
def checker():
    return EvenOddChecker()

@pytest.mark.parametrize("number, expected_even", [
    (0, True),
    (1, False),
    (2, True),
    (-1, False),
    (-2, True)
])
def test_is_even(checker, number, expected_even):
    assert checker.is_even(number) == expected_even

@pytest.mark.parametrize("number, expected_odd", [
    (0, False),
    (1, True),
    (2, False),
    (-1, True),
    (-2, False)
])
def test_is_odd(checker, number, expected_odd):
    assert checker.is_odd(number) == expected_odd

if __name__ == "__main__":
    pytest.main()