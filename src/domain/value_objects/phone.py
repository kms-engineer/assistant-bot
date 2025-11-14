from dataclasses import dataclass
from src.domain.validators.phone_validator import PhoneValidator
from src.domain.value_objects.field import Field


@dataclass
class Phone(Field):

    def __init__(self, raw: str):
        digits = PhoneValidator.normalize(raw)
        PhoneValidator.validate_and_raise(digits)

        super().__init__(digits)
