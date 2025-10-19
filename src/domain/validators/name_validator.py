import re
from typing import Union
from .string_validator import StringValidator


class NameValidator:
    """Validator for name field with comprehensive validation rules."""

    MIN_LENGTH = 2
    MAX_LENGTH = 50

    # Pre-compiled regex pattern for performance
    # Allows letters (any language), spaces, hyphens, and apostrophes
    _NAME_PATTERN = re.compile(r'^[a-zA-ZÀ-ÿ\s\-\']+$')

    # Error message constants
    ERROR_EMPTY = "Name cannot be empty or whitespace"
    ERROR_TOO_SHORT = f"Name must be at least {MIN_LENGTH} characters long"
    ERROR_TOO_LONG = f"Name must be at most {MAX_LENGTH} characters long"
    ERROR_INVALID_CHARS = "Name can only contain letters, spaces, and hyphens"

    @staticmethod
    def validate(name: str) -> Union[str, bool]:
        """
        Validate name field according to business rules.

        Validation rules:
        - Cannot be empty or whitespace only
        - Must be between 2 and 50 characters (after trimming)
        - Only allows letters (including international), spaces, and hyphens
        - Supports names like: "John", "Mary-Jane", "José García"

        Args:
            name: The name string to validate

        Returns:
            True if valid, error message string if invalid

        Examples:
            >>> NameValidator.validate("John Doe")
            True
            >>> NameValidator.validate("A")
            'Name must be at least 2 characters long'
            >>> NameValidator.validate("John123")
            'Name can only contain letters, spaces, and hyphens'
            >>> NameValidator.validate("")
            'Name cannot be empty or whitespace'
        """
        # Check if not empty
        if not StringValidator.is_not_empty(name):
            return NameValidator.ERROR_EMPTY

        # Trim for length validation
        trimmed_name = name.strip()

        # Check minimum length
        if not StringValidator.has_min_length(trimmed_name, NameValidator.MIN_LENGTH):
            return NameValidator.ERROR_TOO_SHORT

        # Check maximum length
        if not StringValidator.has_max_length(trimmed_name, NameValidator.MAX_LENGTH):
            return NameValidator.ERROR_TOO_LONG

        # Format validation: only letters, spaces, hyphens
        if not NameValidator._NAME_PATTERN.fullmatch(trimmed_name):
            return NameValidator.ERROR_INVALID_CHARS

        return True
