import re

from .string_validator import StringValidator
from ..validators.number_validator import NumberValidator

class PhoneValidator:

    @staticmethod
    def validate(phone: str) -> str | bool:
        if not NumberValidator.is_number(phone):
            return "Phone number must contain only digits"
        if not StringValidator.has_length(phone, 10):
            return "Phone number must be exactly 10 digits long"
        return True

    @staticmethod
    def normalize(raw: str) -> str:
        return re.sub(r"\D+", "", raw)
