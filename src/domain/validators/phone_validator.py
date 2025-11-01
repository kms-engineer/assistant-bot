import re
from typing import Union
from src.config import ValidationConfig
from .base_validator import BaseValidator


class PhoneValidator(BaseValidator):

    @staticmethod
    def validate(phone: str) -> Union[str, bool]:
        if not isinstance(phone, str):
            return ValidationConfig.PHONE_ERROR_NOT_STRING

        # Phone can start with + or a digit
        if not phone or len(phone) == 0:
            return ValidationConfig.PHONE_ERROR_EMPTY

        if phone[0] == '+':
            phone = phone[1:]
        if not (all(c.isdigit() for c in phone)):
            return ValidationConfig.PHONE_ERROR_INVALID_FORMAT

        # Extract digits only (skip the + if present)
        digits = ''.join(c for c in phone if c.isdigit())

        # Check length is between 8 and 15 digits
        if len(digits) < ValidationConfig.PHONE_MIN_DIGITS or len(digits) > ValidationConfig.PHONE_MAX_DIGITS:
            return ValidationConfig.PHONE_ERROR_INVALID_LENGTH

        return True

    @staticmethod
    def normalize(raw: str) -> str:
        if not raw:
            return ""
        if raw.startswith('+'):
            return re.sub(r"\D+", '', raw[1:])
        return re.sub(r"\D+", '', raw)