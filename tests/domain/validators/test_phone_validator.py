import pytest
from src.domain.validators.phone_validator import PhoneValidator

# Tests for the normalize method
@pytest.mark.parametrize("raw_phone, expected_normalized", [
    ("(123) 456-7890", "1234567890"),
    ("123.456.7890", "1234567890"),
    ("123 456 7890", "1234567890"),
    ("+1 (123) 456-7890", "11234567890"),
    ("123-456-7890", "1234567890"),
    ("1234567890", "1234567890"), # Already normalized
    ("NoNumbersHere", ""),
    ("", ""),
])
def test_normalize(raw_phone, expected_normalized):
    """Tests that normalize correctly strips non-digit characters."""
    assert PhoneValidator.normalize(raw_phone) == expected_normalized

# Tests for the validate method
def test_validate_with_valid_phone():
    """Tests that a valid 10-digit string passes validation."""
    assert PhoneValidator.validate("1234567890") is True

@pytest.mark.parametrize("invalid_phone, expected_message", [
    ("123456789", "Phone number must be exactly 10 digits long"),
    ("12345678901", "Phone number must be exactly 10 digits long"),
    ("123456789a", "Phone number must contain only digits"),
    ("abcdefghij", "Phone number must contain only digits"),
    ("(123)456-7890", "Phone number must be exactly 10 digits long"),
    ("   1234567890 ", "Phone number must be exactly 10 digits long"),
])
def test_validate_with_invalid_phone_strings(invalid_phone, expected_message):
    """Tests various invalid phone number strings."""
    assert PhoneValidator.validate(invalid_phone) == expected_message

@pytest.mark.parametrize("non_string_input", [
    None,
    True,
    [],
    {},
])
def test_validate_with_non_string_input(non_string_input):
    """Tests that non-string inputs fail validation."""
    assert PhoneValidator.validate(non_string_input) == "Phone number must be string value"
