import re
from typing import Union
from .string_validator import StringValidator


class AddressValidator:
    """Validator for address field with comprehensive validation rules."""

    MIN_LENGTH = 5
    MAX_LENGTH = 200

    # Pre-compiled regex patterns for performance
    _ADDRESS_PATTERN = re.compile(r'^(?=.*[a-zA-Z0-9])[a-zA-Z0-9\s.,/\-#]+$')

    # Error message constants
    ERROR_EMPTY = "Address cannot be empty or whitespace"
    ERROR_TOO_SHORT = f"Address must be at least {MIN_LENGTH} characters long"
    ERROR_TOO_LONG = f"Address must be at most {MAX_LENGTH} characters long"
    ERROR_INVALID_CHARS = "Address contains invalid characters. Only letters, numbers, spaces, and basic punctuation (.,/-#) are allowed"

    @staticmethod
    def validate(address: str) -> Union[str, bool]:
        """
        Validate address field according to business rules.

        Validation rules:
        - Cannot be empty or whitespace only
        - Must be between 5 and 200 characters (after trimming)
        - Must contain at least one alphanumeric character
        - Only allows letters, numbers, spaces, and punctuation (.,/-#)

        Args:
            address: The address string to validate

        Returns:
            True if valid, error message string if invalid

        Examples:
            >>> AddressValidator.validate("123 Main Street")
            True
            >>> AddressValidator.validate("ab")
            'Address must be at least 5 characters long'
            >>> AddressValidator.validate("")
            'Address cannot be empty or whitespace'
        """
        # Check if not empty
        if not StringValidator.is_not_empty(address):
            return AddressValidator.ERROR_EMPTY

        # Trim for length validation
        trimmed_address = address.strip()

        # Check minimum length
        if not StringValidator.has_min_length(trimmed_address, AddressValidator.MIN_LENGTH):
            return AddressValidator.ERROR_TOO_SHORT

        # Check maximum length
        if not StringValidator.has_max_length(trimmed_address, AddressValidator.MAX_LENGTH):
            return AddressValidator.ERROR_TOO_LONG

        # Combined format validation: checks both allowed characters and alphanumeric requirement
        # Pattern uses positive lookahead (?=.*[a-zA-Z0-9]) to ensure at least one alphanumeric
        if not AddressValidator._ADDRESS_PATTERN.fullmatch(trimmed_address):
            return AddressValidator.ERROR_INVALID_CHARS

        return True
