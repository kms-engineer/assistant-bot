from .string_validator import StringValidator


class NameValidator:
    MAX_LENGTH = 25

    @staticmethod
    def validate(value):
        """
        Validates a name value.

        Returns:
            True if valid, or an error message string if invalid
        """
        # Check if value is a string
        if not StringValidator.is_string(value):
            return "Name must be a string"

        # Check if empty or whitespace
        if StringValidator.is_empty(value):
            return "Name cannot be empty or whitespace"

        # Check max length
        if len(value) > NameValidator.MAX_LENGTH:
            return f"Name cannot exceed {NameValidator.MAX_LENGTH} characters"

        return True
