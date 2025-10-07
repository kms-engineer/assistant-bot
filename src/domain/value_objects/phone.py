from dataclasses import dataclass
from ..validators.phone_validator import PhoneValidator
from .field import Field


@dataclass
class Phone(Field):

    def __init__(self, raw: str):
        digits = PhoneValidator.normalize(raw)
        if not PhoneValidator.validate(digits):
            raise ValueError(
                f"Invalid phone number: '{raw}'. Expected exactly 10 digits after normalization."
            )
        super().__init__(digits)
