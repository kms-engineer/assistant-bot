import pytest
from src.domain.value_objects.address import Address

def test_address_creation_with_valid_address():
    """Tests that an Address object is created successfully with a valid address."""
    valid_address_str = "123 Main St"
    address_obj = Address(valid_address_str)
    assert address_obj.value == "123 Main St"

def test_address_creation_strips_whitespace():
    """Tests that leading/trailing whitespace is stripped from a valid address."""
    address_with_spaces = "  456 Oak Avenue  "
    address_obj = Address(address_with_spaces)
    assert address_obj.value == "456 Oak Avenue"

@pytest.mark.parametrize("invalid_address, expected_error_message", [
    ("", "Address cannot be empty or whitespace"),
    ("   ", "Address cannot be empty or whitespace"),
    ("a" * 201, "Address must be at most 200 characters long"),
    (12345, "Address cannot be empty or whitespace"),
    (None, "Address cannot be empty or whitespace"),
])
def test_address_creation_with_invalid_address(invalid_address, expected_error_message):
    """
    Tests that creating an Address with invalid input raises a ValueError
    with the correct message from the validator.
    """
    with pytest.raises(ValueError) as excinfo:
        Address(invalid_address)
    assert str(excinfo.value) == expected_error_message
