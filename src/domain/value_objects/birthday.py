from dataclasses import dataclass
from ..validators.birthday_validator import BirthdayValidator
from .field import Field


@dataclass
class Birthday(Field):

    def __init__(self, value: str):
        validate_result = BirthdayValidator.validate(value)
        if validate_result is not True:
            raise ValueError(str(validate_result))
        super().__init__(value)
