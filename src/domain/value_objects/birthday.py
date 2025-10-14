from dataclasses import dataclass
from ..validators.birthday_validator import BirthdayValidator
from .field import Field


@dataclass
class Birthday(Field):

    def __init__(self, value: str):
        BirthdayValidator.validate(value)
        super().__init__(value)
