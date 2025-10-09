from ..validators.phone_validator import PhoneValidator
from .field import Field


class Phone(Field):

    def __init__(self, raw: str):
        digits = PhoneValidator.normalize(raw)
        if not PhoneValidator.validate(digits):
            raise ValueError(
                f"Invalid phone number: '{raw}'. Expected 9-15 digits after normalization."
            )
        super().__init__(digits)

    @staticmethod
    def normalize(raw: str) -> str:
        return PhoneValidator.normalize(raw)

    @staticmethod
    def validate(phone: str) -> bool:
        return PhoneValidator.validate(phone)
