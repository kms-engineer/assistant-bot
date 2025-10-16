import re


class StringValidator:

    @staticmethod
    def is_string(value: any) -> bool:
        """Check if value is a string."""
        return isinstance(value, str)

    @staticmethod
    def is_empty(value: any) -> bool:
        """Check if value is None, empty string, or whitespace only."""
        if value is None:
            return True
        if not isinstance(value, str):
            return False
        return len(value.strip()) == 0

    @staticmethod
    def is_not_empty(value: any) -> bool:
        """Check if value is not empty (inverse of is_empty)."""
        return not StringValidator.is_empty(value)

    @staticmethod
    def has_min_length(value: str, min_length: int) -> bool:
        """Check if string has at least min_length characters."""
        if not isinstance(value, str):
            return False
        return len(value) >= min_length

    @staticmethod
    def has_max_length(value: str, max_length: int) -> bool:
        """Check if string has at most max_length characters."""
        if not isinstance(value, str):
            return False
        return len(value) <= max_length

    @staticmethod
    def has_length(value: str, length: int) -> bool:
        """Check if string has exactly length characters."""
        if not isinstance(value, str):
            return False
        return len(value) == length

    @staticmethod
    def matches_pattern(value: str, pattern: str) -> bool:
        """Check if string matches the regex pattern (partial match allowed)."""
        if not isinstance(value, str):
            return False
        return re.search(pattern, value) is not None

    @staticmethod
    def exactly_match_pattern(value: str, pattern: str) -> bool:
        """Check if string exactly matches the regex pattern (full match required)."""
        if not isinstance(value, str):
            return False
        return re.fullmatch(pattern, value) is not None
