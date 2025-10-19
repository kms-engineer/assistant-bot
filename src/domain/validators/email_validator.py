import re
from typing import Union
from .string_validator import StringValidator


class EmailValidator:
    """Validator for email field with comprehensive validation rules."""

    # Pre-compiled regex pattern for email validation
    # Basic email pattern: localpart@domain.tld
    _EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )

    # Error message constants
    ERROR_EMPTY = "Email cannot be empty or whitespace"
    ERROR_INVALID_FORMAT = "Email must be a valid email address (e.g., user@example.com)"

    @staticmethod
    def validate(email: str) -> Union[str, bool]:
        """
        Validate email field according to business rules.

        Validation rules:
        - Cannot be empty or whitespace only
        - Must match standard email format: localpart@domain.tld
        - Allows alphanumeric, dots, underscores, percent, plus, and hyphens in local part
        - Domain must have at least one dot and valid TLD

        Args:
            email: The email string to validate

        Returns:
            True if valid, error message string if invalid

        Examples:
            >>> EmailValidator.validate("user@example.com")
            True
            >>> EmailValidator.validate("invalid-email")
            'Email must be a valid email address (e.g., user@example.com)'
            >>> EmailValidator.validate("")
            'Email cannot be empty or whitespace'
        """
        # Check if not empty
        if not StringValidator.is_not_empty(email):
            return EmailValidator.ERROR_EMPTY

        # Trim and convert to lowercase for validation
        trimmed_email = email.strip().lower()

        # Format validation: must match email pattern
        if not EmailValidator._EMAIL_PATTERN.fullmatch(trimmed_email):
            return EmailValidator.ERROR_INVALID_FORMAT

        return True
