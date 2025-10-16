import re
from .string_validator import StringValidator


class AddressValidator:

    MIN_LENGTH = 5
    MAX_LENGTH = 200

    @staticmethod
    def validate(address: str) -> str | bool:
        """
        Validate address field with the following rules:
        - Must be a string
        - Cannot be empty or whitespace only
        - Must be between 5 and 200 characters
        - Must match basic address format (alphanumeric with common punctuation)

        Returns True if valid, error message string if invalid.
        """
        # Check if it's a string
        if not StringValidator.is_string(address):
            return "Address must be a string value"

        # Check if not empty
        if not StringValidator.is_not_empty(address):
            return "Address cannot be empty or whitespace"

        # Trim for length validation
        trimmed_address = address.strip()

        # Check minimum length
        if not StringValidator.has_min_length(trimmed_address, AddressValidator.MIN_LENGTH):
            return f"Address must be at least {AddressValidator.MIN_LENGTH} characters long"

        # Check maximum length
        if not StringValidator.has_max_length(trimmed_address, AddressValidator.MAX_LENGTH):
            return f"Address must be at most {AddressValidator.MAX_LENGTH} characters long"

        # Basic format validation: allows letters, digits, spaces, and common punctuation (.,/-#)
        # Address should contain at least some alphanumeric characters
        address_pattern = r'^[a-zA-Z0-9\s.,/\-#]+$'
        if not StringValidator.exactly_match_pattern(trimmed_address, address_pattern):
            return "Address contains invalid characters. Only letters, numbers, spaces, and basic punctuation (.,/-#) are allowed"

        # Check that address contains at least one alphanumeric character
        if not re.search(r'[a-zA-Z0-9]', trimmed_address):
            return "Address must contain at least one letter or number"

        return True
