import unittest
import pytest
from simple_math import SimpleMath


@pytest.fixture
def test_math():
    return SimpleMath()


def test_square_positive(test_math):
    assert test_math.square(2) == 4


def test_square_zero(test_math):
    assert test_math.square(0) == 0


def test_square_negative(test_math):
    assert test_math.square(-2) == 4


def test_cube_positive(test_math):
    assert test_math.cube(2) == 8
    assert test_math.cube(3) == 27


def test_cube_zero(test_math):
    assert test_math.cube(0) == 0


def test_cube_negative(test_math):
    assert test_math.cube(-2) == 8


if __name__ == '__main__':
    unittest.main()
