import re
from typing import Any


class StringValidator:

    @staticmethod
    def is_string(value: Any) -> bool:
        return isinstance(value, str)

    @staticmethod
    def is_empty(value: Any) -> bool:
        if value is None:
            return True
        if not isinstance(value, str):
            return False
        return len(value.strip()) == 0

    @staticmethod
    def is_not_empty(value: Any) -> bool:
        return not StringValidator.is_empty(value)

    @staticmethod
    def has_min_length(value: str, min_length: int) -> bool:
        if not isinstance(value, str):
            return False
        return len(value) >= min_length

    @staticmethod
    def has_max_length(value: str, max_length: int) -> bool:
        if not isinstance(value, str):
            return False
        return len(value) <= max_length

    @staticmethod
    def has_length(value: str, length: int) -> bool:
        if not isinstance(value, str):
            return False
        return len(value) == length

    @staticmethod
    def matches_pattern(value: str, pattern: str) -> bool:
        if not isinstance(value, str):
            return False
        return re.search(pattern, value) is not None

    @staticmethod
    def exactly_match_pattern(value: str, pattern: str) -> bool:
        if not isinstance(value, str):
            return False
        return re.fullmatch(pattern, value) is not None
