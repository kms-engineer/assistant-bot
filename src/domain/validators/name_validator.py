import re
from typing import Union

from src.config import ValidationConfig, RegexPatterns
from src.domain.validators.base_validator import BaseValidator


class NameValidator(BaseValidator):
    _NAME_PATTERN = re.compile(RegexPatterns.VALIDATION_NAME_PATTERN)

    @staticmethod
    def validate(name: str) -> Union[str, bool]:
        if BaseValidator.is_empty_string(name):
            return ValidationConfig.NAME_ERROR_EMPTY

        trimmed_name = name.strip()

        if len(trimmed_name) < ValidationConfig.NAME_MIN_LENGTH:
            return ValidationConfig.NAME_ERROR_TOO_SHORT

        if len(trimmed_name) > ValidationConfig.NAME_MAX_LENGTH:
            return ValidationConfig.NAME_ERROR_TOO_LONG

        if not NameValidator._NAME_PATTERN.fullmatch(trimmed_name):
            return ValidationConfig.NAME_ERROR_INVALID_CHARS

        return True
