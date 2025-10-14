import pytest
from src.domain.validators.name_validator import NameValidator

@pytest.mark.parametrize("valid_name", [
    "John Doe",
    "Jane",
    "a" * 25,  # Test boundary condition for max length
    "A name with spaces",
])
def test_validate_with_valid_name(valid_name):
    """Tests that a valid name passes validation."""
    assert NameValidator.validate(valid_name) is True

@pytest.mark.parametrize("invalid_input, expected_message", [
    (123, "Name must be a string"),
    (None, "Name must be a string"),
    (True, "Name must be a string"),
    (["John"], "Name must be a string"),
    ({"name": "John"}, "Name must be a string"),
])
def test_validate_with_non_string_input(invalid_input, expected_message):
    """Tests that non-string inputs return the correct error message."""
    assert NameValidator.validate(invalid_input) == expected_message

@pytest.mark.parametrize("empty_name", [
    "",
    "   ",
    "\t\n"
])
def test_validate_with_empty_or_whitespace_name(empty_name):
    """Tests that an empty or whitespace-only name returns an error."""
    assert NameValidator.validate(empty_name) == "Name cannot be empty or whitespace"

def test_validate_with_long_name():
    """Tests that a name exceeding the max length returns an error."""
    long_name = "a" * 26
    assert NameValidator.validate(long_name) == "Name cannot exceed 25 characters"
