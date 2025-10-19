import re
from typing import Any


class StringValidator:
    """Utility class for string validation operations."""

    @staticmethod
    def is_string(value: Any) -> bool:
        """
        Check if value is a string.

        Args:
            value: The value to check

        Returns:
            True if value is a string, False otherwise

        Examples:
            >>> StringValidator.is_string("hello")
            True
            >>> StringValidator.is_string(123)
            False
        """
        return isinstance(value, str)

    @staticmethod
    def is_empty(value: Any) -> bool:
        """
        Check if value is None, empty string, or whitespace only.

        Args:
            value: The value to check

        Returns:
            True if empty/None/whitespace, False otherwise

        Examples:
            >>> StringValidator.is_empty("")
            True
            >>> StringValidator.is_empty("  ")
            True
            >>> StringValidator.is_empty("hello")
            False
        """
        if value is None:
            return True
        if not isinstance(value, str):
            return False
        return len(value.strip()) == 0

    @staticmethod
    def is_not_empty(value: Any) -> bool:
        """
        Check if value is not empty (inverse of is_empty).

        Args:
            value: The value to check

        Returns:
            True if not empty, False otherwise

        Examples:
            >>> StringValidator.is_not_empty("hello")
            True
            >>> StringValidator.is_not_empty("")
            False
        """
        return not StringValidator.is_empty(value)

    @staticmethod
    def has_min_length(value: str, min_length: int) -> bool:
        """
        Check if string has at least min_length characters.

        Args:
            value: The string to check
            min_length: Minimum required length

        Returns:
            True if string meets minimum length, False otherwise

        Examples:
            >>> StringValidator.has_min_length("hello", 5)
            True
            >>> StringValidator.has_min_length("hi", 5)
            False
        """
        if not isinstance(value, str):
            return False
        return len(value) >= min_length

    @staticmethod
    def has_max_length(value: str, max_length: int) -> bool:
        """
        Check if string has at most max_length characters.

        Args:
            value: The string to check
            max_length: Maximum allowed length

        Returns:
            True if string meets maximum length, False otherwise

        Examples:
            >>> StringValidator.has_max_length("test", 4)
            True
            >>> StringValidator.has_max_length("testing", 4)
            False
        """
        if not isinstance(value, str):
            return False
        return len(value) <= max_length

    @staticmethod
    def has_length(value: str, length: int) -> bool:
        """
        Check if string has exactly length characters.

        Args:
            value: The string to check
            length: Required exact length

        Returns:
            True if string has exact length, False otherwise

        Examples:
            >>> StringValidator.has_length("exact", 5)
            True
            >>> StringValidator.has_length("exact", 4)
            False
        """
        if not isinstance(value, str):
            return False
        return len(value) == length

    @staticmethod
    def matches_pattern(value: str, pattern: str) -> bool:
        """
        Check if string matches the regex pattern (partial match allowed).

        Args:
            value: The string to check
            pattern: Regular expression pattern

        Returns:
            True if pattern found in string, False otherwise

        Examples:
            >>> StringValidator.matches_pattern("abcde", r"^abc")
            True
            >>> StringValidator.matches_pattern("abcde", r"xyz")
            False
        """
        if not isinstance(value, str):
            return False
        return re.search(pattern, value) is not None

    @staticmethod
    def exactly_match_pattern(value: str, pattern: str) -> bool:
        """
        Check if string exactly matches the regex pattern (full match required).

        Args:
            value: The string to check
            pattern: Regular expression pattern

        Returns:
            True if entire string matches pattern, False otherwise

        Examples:
            >>> StringValidator.exactly_match_pattern("abcde", r"abcde")
            True
            >>> StringValidator.exactly_match_pattern("abc", r"abcde")
            False
        """
        if not isinstance(value, str):
            return False
        return re.fullmatch(pattern, value) is not None
