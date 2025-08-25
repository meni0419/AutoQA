from isAdult import AgeValidator
import pytest

@pytest.fixture
def validator():
    return AgeValidator()

@pytest.mark.parametrize("age, expected", [
    (18, True),
    (17, False),
    (19, True)
])

def test_age_is_adult(validator, age, expected):
    assert validator.is_adult(age) == expected
