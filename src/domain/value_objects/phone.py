from dataclasses import dataclass
from ..validators.phone_validator import PhoneValidator
from .field import Field


@dataclass
class Phone(Field):

    def __init__(self, raw: str):
        digits = PhoneValidator.normalize(raw)
        validation_result = PhoneValidator.validate(digits)
        if validation_result is not True:
            raise ValueError(str(validation_result))

        super().__init__(digits)
