from dataclasses import dataclass
from ..validators.email_validator import EmailValidator
from .field import Field


@dataclass
class Email(Field):

    def __init__(self, value: str):
        if not EmailValidator.validate(value):
            raise ValueError(f"Invalid email format: '{value}'")
        super().__init__(value)
