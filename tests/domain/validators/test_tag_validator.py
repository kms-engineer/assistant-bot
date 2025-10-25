import pytest
from src.domain.validators.tag_validator import TagValidator

@pytest.mark.parametrize("valid_tag", [
    "python",
    "pytest",
    "a" * 50, # Test boundary condition for max length
])
def test_validate_with_valid_tag(valid_tag):
    """Tests that a valid tag passes validation."""
    assert TagValidator.validate(valid_tag) is True

@pytest.mark.parametrize("invalid_input, expected_message", [
    (123, "Tag must be a string"),
    (None, "Tag must be a string"),
    ([], "Tag must be a string"),
    ({}, "Tag must be a string"),
    (True, "Tag must be a string"),
])
def test_validate_with_non_string(invalid_input, expected_message):
    """Tests that a non-string input returns an error message."""
    assert TagValidator.validate(invalid_input) == expected_message

@pytest.mark.parametrize("empty_value", [
    "",
    "   ",
    "\t\n",
])
def test_validate_with_empty_or_whitespace(empty_value):
    """Tests that an empty or whitespace string returns an error message."""
    assert TagValidator.validate(empty_value) == "Tag cannot be empty"

def test_validate_with_long_tag():
    """Tests that a tag longer than 50 characters returns an error message."""
    long_tag = "a" * 51
    assert TagValidator.validate(long_tag) == "Tag cannot be longer than 50 characters"
