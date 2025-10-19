import re
from .string_validator import StringValidator


class EmailValidator:
    MAX_LENGTH = 100
    # Basic email regex pattern
    EMAIL_PATTERN = r'^[a-zA-Z0-9][a-zA-Z0-9._-]*@[a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,}$'

    @staticmethod
    def validate(value):
        """
        Validates an email address.

        Returns:
            True if valid, or an error message string if invalid
        """
        # Check if value is a string
        if not StringValidator.is_string(value):
            return "Email must be a string"

        # Check if empty or whitespace
        if StringValidator.is_empty(value):
            return "Email cannot be empty or whitespace"

        # Check max length
        if len(value) > EmailValidator.MAX_LENGTH:
            return f"Email cannot exceed {EmailValidator.MAX_LENGTH} characters. Current length: {len(value)}"

        # Check email format
        if not re.match(EmailValidator.EMAIL_PATTERN, value):
            return f"Email format is invalid. Current value: {value}"

        return True
