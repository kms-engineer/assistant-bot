import pytest
from src.domain.value_objects.email import Email


@pytest.mark.parametrize(
    "valid_email",
    [
        "test@example.com",
        "firstname.lastname@example.co.uk",
        "user+alias@sub.domain.org",
        "12345@numeric.net",
        "a" * 89 + "@a.co",  # Test near the length limit
    ],
)
def test_email_creation_with_valid_email(valid_email):
    """Tests that an Email object is created successfully with various valid emails."""
    email_obj = Email(valid_email)
    assert email_obj.value == valid_email


@pytest.mark.parametrize(
    "invalid_input, expected_error_message",
    [
        # Type and presence checks
        (None, "Email cannot be empty or whitespace"),
        (12345, "Email cannot be empty or whitespace"),
        ("", "Email cannot be empty or whitespace"),
        ("   ", "Email cannot be empty or whitespace"),
        # Length check
        ("a" * 90 + "@domain.com", "Email must be at most 100 characters long"),
        # Format checks from the validator pattern
        (
            "plainaddress",
            "Email must be a valid email address (e.g., user@example.com)",
        ),
        ("@domain.com", "Email must be a valid email address (e.g., user@example.com)"),
        ("user@", "Email must be a valid email address (e.g., user@example.com)"),
        ("user@.com", "Email must be a valid email address (e.g., user@example.com)"),
        (
            "user@domain..com",
            "Email must be a valid email address (e.g., user@example.com)",
        ),
        (
            "user@domain.c",
            "Email must be a valid email address (e.g., user@example.com)",
        ),
    ],
)
def test_email_creation_with_invalid_input(invalid_input, expected_error_message):
    """
    Tests that creating an Email with various invalid inputs raises a ValueError
    with the correct error message from the validator.
    """
    with pytest.raises(ValueError) as excinfo:
        Email(invalid_input)
    assert str(excinfo.value) == expected_error_message
