import re

from .string_validator import StringValidator
from ..validators.number_validator import NumberValidator

class PhoneValidator:

    @staticmethod
    def validate(phone: str) -> str | bool:
        if not StringValidator.is_string(phone):
            return "Phone number must be string value"
        phone = PhoneValidator.normalize(phone)
        if not StringValidator.has_length(phone, 10):
            return "Phone number must be exactly 10 digits long"
        if not NumberValidator.is_number(phone):
            return "Phone number must contain only digits"
        return True

    @staticmethod
    def normalize(raw: str) -> str:
        if raw.startswith('+'):
            normalized = '+' + re.sub(r"\D+", '', raw[1:])
        else:
            normalized = re.sub(r"\D+", '', raw)
        return normalized