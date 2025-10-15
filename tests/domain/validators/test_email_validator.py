import pytest
from src.domain.validators.email_validator import EmailValidator

@pytest.mark.parametrize("valid_email", [
    "test@example.com",
    "test.name@example.co.uk",
    "user123@sub.domain.org",
    "a" * 87 + "@example.com",  # Test boundary: 100 characters total
])
def test_validate_with_valid_email(valid_email):
    """Tests that a valid email address passes validation."""
    assert EmailValidator.validate(valid_email) is True

@pytest.mark.parametrize("invalid_input, expected_message", [
    (12345, "Email must be a string"),
    (None, "Email must be a string"),
    (True, "Email must be a string"),
    ([], "Email must be a string"),
])
def test_validate_with_non_string_input(invalid_input, expected_message):
    """Tests that non-string inputs are rejected."""
    assert EmailValidator.validate(invalid_input) == expected_message

@pytest.mark.parametrize("empty_input", ["", "   ", "\t\n"])
def test_validate_with_empty_or_whitespace(empty_input):
    """Tests that empty or whitespace-only strings are rejected."""
    assert EmailValidator.validate(empty_input) == "Email cannot be empty or whitespace"

def test_validate_with_too_long_email():
    """Tests that an email exceeding 100 characters is rejected."""
    long_email = "a" * 89 + "@example.com"  # 101 characters
    expected_message = f"Email cannot exceed 100 characters. Current length: {len(long_email)}"
    assert EmailValidator.validate(long_email) == expected_message

@pytest.mark.parametrize("invalid_format_email", [
    "plainaddress",
    "@missingusername.com",
    "username@.com",
    "username@domain.",
    "username@domain.c",
    "username@domain..com",
    "username domain@email.com",
])
def test_validate_with_invalid_format(invalid_format_email):
    """Tests various incorrectly formatted email addresses."""
    expected_message = f"Email format is invalid. Current value: {invalid_format_email}"
    assert EmailValidator.validate(invalid_format_email) == expected_message
