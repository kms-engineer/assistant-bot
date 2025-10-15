import pytest
from src.domain.value_objects.email import Email

@pytest.mark.parametrize("valid_email", [
    "test@example.com",
    "firstname.lastname@example.co.uk",
    "user+alias@sub.domain.org",
    "12345@numeric.net",
    "a" * 89 + "@a.co", # Test near the length limit
])
def test_email_creation_with_valid_email(valid_email):
    """Tests that an Email object is created successfully with various valid emails."""
    email_obj = Email(valid_email)
    assert email_obj.value == valid_email

@pytest.mark.parametrize("invalid_input, expected_error_message", [
    # Type and presence checks
    (None, "Email must be a string"),
    (12345, "Email must be a string"),
    ("", "Email cannot be empty or whitespace"),
    ("   ", "Email cannot be empty or whitespace"),

    # Length check
    ("a" * 90 + "@domain.com", "Email cannot exceed 100 characters. Current length: 101"),

    # Format checks from the validator pattern
    ("plainaddress", "Email format is invalid. Current value: plainaddress"),
    ("@domain.com", "Email format is invalid. Current value: @domain.com"),
    ("user@", "Email format is invalid. Current value: user@"),
    ("user@.com", "Email format is invalid. Current value: user@.com"),
    ("user@domain..com", "Email format is invalid. Current value: user@domain..com"),
    ("user@domain.c", "Email format is invalid. Current value: user@domain.c"),
])
def test_email_creation_with_invalid_input(invalid_input, expected_error_message):
    """
    Tests that creating an Email with various invalid inputs raises a ValueError
    with the correct error message from the validator.
    """
    with pytest.raises(ValueError) as excinfo:
        Email(invalid_input)
    assert str(excinfo.value) == expected_error_message
