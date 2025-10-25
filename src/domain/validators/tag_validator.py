class TagValidator:
    """Utility class for tag validation operations."""

    @staticmethod
    def validate(value: str) -> bool | str:
        """
        Validates a tag value.

        Requirements:
        - Non-empty after trimming
        - Length <= 50 characters

        Args:
            value: The tag string to validate

        Returns:
            True if valid, error message string if invalid
        """
        if not isinstance(value, str):
            return "Tag must be a string"

        trimmed = value.strip()

        if not trimmed:
            return "Tag cannot be empty"

        if len(trimmed) > 50:
            return "Tag cannot be longer than 50 characters"

        return True
