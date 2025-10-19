import pytest
from src.domain.validators.number_validator import NumberValidator

# Tests for is_positive
@pytest.mark.parametrize("number, expected", [
    (1, True),
    (100, True),
    (0, False),
    (-1, False),
    (-100, False),
])
def test_is_positive(number, expected):
    """Test the is_positive method."""
    assert NumberValidator.is_positive(number) == expected

# Tests for is_negative
@pytest.mark.parametrize("number, expected", [
    (-1, True),
    (-100, True),
    (0, False),
    (1, False),
    (100, False),
])
def test_is_negative(number, expected):
    """Test the is_negative method."""
    assert NumberValidator.is_negative(number) == expected

# Tests for is_zero
@pytest.mark.parametrize("number, expected", [
    (0, True),
    (1, False),
    (-1, False),
    (100, False),
])
def test_is_zero(number, expected):
    """Test the is_zero method."""
    assert NumberValidator.is_zero(number) == expected

# Tests for is_between
@pytest.mark.parametrize("number, minimum, maximum, expected", [
    (5, 1, 10, True),
    (1, 1, 10, True),   # Lower boundary
    (10, 1, 10, True),  # Upper boundary
    (0, 1, 10, False),  # Below range
    (11, 1, 10, False), # Above range
    (-5, -10, -1, True),# Negative range
    (0, 0, 0, True),    # Zero range
])
def test_is_between(number, minimum, maximum, expected):
    """Test the is_between method with various ranges."""
    assert NumberValidator.is_between(number, minimum, maximum) == expected

# Tests for is_number
@pytest.mark.parametrize("value, expected", [
    ("12345", True),
    ("0", True),
    ("123a", False),
    ("-123", False), # isdigit is False for negative signs
    ("12.34", False),# isdigit is False for decimals
    (" 123 ", False),# isdigit is False for whitespace
    ("", False),
    (None, False),
])
def test_is_number(value, expected):
    """Test the is_number method for string inputs."""
    assert NumberValidator.is_number(value) == expected
