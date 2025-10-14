import pytest
from src.domain.validators.address_validator import AddressValidator

@pytest.mark.parametrize("valid_address", [
    "123 Main St, Anytown, USA",
    "PO Box 456",
    "Apartment 7B, 459 Broadway",
    "a" * 200,  # Boundary: Exactly 200 characters
])
def test_validate_with_valid_address(valid_address):
    """Tests that a valid address string passes validation."""
    assert AddressValidator.validate(valid_address) is True

@pytest.mark.parametrize("invalid_input, expected_message", [
    (12345, "Address must be a string"),
    (None, "Address must be a string"),
    (True, "Address must be a string"),
    ({}, "Address must be a string"),
])
def test_validate_with_non_string_input(invalid_input, expected_message):
    """Tests that non-string inputs are rejected."""
    assert AddressValidator.validate(invalid_input) == expected_message

@pytest.mark.parametrize("empty_input", ["", "   ", "\t\n"])
def test_validate_with_empty_or_whitespace(empty_input):
    """Tests that empty or whitespace-only strings are rejected."""
    assert AddressValidator.validate(empty_input) == "Address cannot be empty or whitespace"

def test_validate_with_too_long_address():
    """Tests that an address exceeding 200 characters is rejected."""
    long_address = "a" * 201
    expected_message = "Address cannot exceed 200 characters"
    assert AddressValidator.validate(long_address) == expected_message
