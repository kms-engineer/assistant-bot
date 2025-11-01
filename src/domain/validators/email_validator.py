import re
from typing import Union
from src.config import RegexPatterns, ValidationConfig
from .base_validator import BaseValidator


class EmailValidator(BaseValidator):

    _EMAIL_PATTERN = re.compile(RegexPatterns.VALIDATION_EMAIL_PATTERN)

    @staticmethod
    def validate(email: str) -> Union[str, bool]:
        if not isinstance(email, str) or not email or len(email.strip()) == 0:
            return ValidationConfig.EMAIL_ERROR_EMPTY

        trimmed_email = email.strip().lower()

        if len(trimmed_email) > ValidationConfig.EMAIL_MAX_LENGTH:
            return ValidationConfig.EMAIL_ERROR_TOO_LONG

        if not EmailValidator._EMAIL_PATTERN.fullmatch(trimmed_email):
            return ValidationConfig.EMAIL_ERROR_INVALID_FORMAT

        return True
