import pytest
from src.domain.validators.string_validator import StringValidator

# Tests for is_string
@pytest.mark.parametrize("value, expected", [
    ("hello", True),
    ("", True),
    ("123", True),
    (123, False),
    (12.3, False),
    (True, False),
    (None, False),
    ([], False),
    ({}, False),
])
def test_is_string(value, expected):
    """Test the is_string method with various data types."""
    assert StringValidator.is_string(value) == expected

# Tests for is_empty
@pytest.mark.parametrize("value, expected", [
    ("", True),
    ("   ", True),
    ("\t\n", True),
    (None, True),
    ("hello", False),
    ("  hello  ", False),
    ("1", False),
])
def test_is_empty(value, expected):
    """Test the is_empty method with empty, whitespace, and non-empty strings."""
    assert StringValidator.is_empty(value) == expected

# Tests for is_not_empty
@pytest.mark.parametrize("value, expected", [
    ("hello", True),
    ("  hello  ", True),
    ("1", True),
    ("", False),
    ("   ", False),
    ("\t\n", False),
    (None, False),
])
def test_is_not_empty(value, expected):
    """Test the is_not_empty method."""
    assert StringValidator.is_not_empty(value) == expected

# Tests for has_min_length
@pytest.mark.parametrize("value, min_length, expected", [
    ("hello", 5, True),
    ("hello", 4, True),
    ("world", 6, False),
    ("", 0, True),
    ("", 1, False),
])
def test_has_min_length(value, min_length, expected):
    """Test the has_min_length method."""
    assert StringValidator.has_min_length(value, min_length) == expected

# Tests for has_max_length
@pytest.mark.parametrize("value, max_length, expected", [
    ("test", 4, True),
    ("test", 5, True),
    ("testing", 6, False),
    ("", 0, True),
])
def test_has_max_length(value, max_length, expected):
    """Test the has_max_length method."""
    assert StringValidator.has_max_length(value, max_length) == expected

# Tests for has_length
@pytest.mark.parametrize("value, length, expected", [
    ("exact", 5, True),
    ("exact", 4, False),
    ("exact", 6, False),
    ("", 0, True),
])
def test_has_length(value, length, expected):
    """Test the has_length method."""
    assert StringValidator.has_length(value, length) == expected

# Tests for matches_pattern
@pytest.mark.parametrize("value, pattern, expected", [
    ("abcde", r"^abc", True),
    ("abcde", r"abc", True),
    ("abcde", r"xyz", False),
    ("123-456", r"\d{3}-\d{3}", True),
    ("hello 123", r"\w+", True), # re.match only checks the beginning
])
def test_matches_pattern(value, pattern, expected):
    """Test the matches_pattern method."""
    assert StringValidator.matches_pattern(value, pattern) == expected

# Tests for exactly_match_pattern
@pytest.mark.parametrize("value, pattern, expected", [
    ("abcde", r"abcde", True),
    ("abcde", r"^abcde$", True),
    ("abc", r"abcde", False), # Does not match fully
    ("hello 123", r"\w+", False), # Does not match the whole string
    ("user@example.com", r"[\w.-]+@[\w.-]+", True),
    ("not-an-email", r"[\w.-]+@[\w.-]+", False),
])
def test_exactly_match_pattern(value, pattern, expected):
    """Test the exactly_match_pattern method."""
    assert StringValidator.exactly_match_pattern(value, pattern) == expected
