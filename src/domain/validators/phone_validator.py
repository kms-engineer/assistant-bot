import re
from typing import Union
from src.config import ValidationConfig, PhoneConfig
from .base_validator import BaseValidator


class PhoneValidator(BaseValidator):

    @staticmethod
    def validate(phone: str) -> Union[str, bool]:
        if not isinstance(phone, str):
            return ValidationConfig.PHONE_ERROR_NOT_STRING
        if len(phone) != PhoneConfig.EXACT_PHONE_LENGTH:
            return ValidationConfig.PHONE_ERROR_INVALID_LENGTH
        if not phone.isdigit():
            return ValidationConfig.PHONE_ERROR_NOT_DIGITS
        return True

    @staticmethod
    def normalize(raw: str) -> str:
        if not raw:
            return ""
        if raw.startswith('+'):
            return re.sub(r"\D+", '', raw[1:])
        return re.sub(r"\D+", '', raw)