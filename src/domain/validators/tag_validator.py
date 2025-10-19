from .string_validator import StringValidator


class TagValidator:
    MAX_LENGTH = 50

    @staticmethod
    def validate(value):
        """
        Validates a tag value.

        Returns:
            True if valid, or an error message string if invalid
        """
        # Check if value is a string
        if not StringValidator.is_string(value):
            return "Tag must be a string"

        # Check if empty or whitespace
        if StringValidator.is_empty(value):
            return "Tag cannot be empty"

        # Check max length
        if not StringValidator.has_max_length(value, TagValidator.MAX_LENGTH):
            return f"Tag too long (max {TagValidator.MAX_LENGTH} characters)"

        return True
