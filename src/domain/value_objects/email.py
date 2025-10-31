from dataclasses import dataclass
from ..validators.email_validator import EmailValidator
from .field import Field


@dataclass
class Email(Field):

    def __init__(self, value: str):
        EmailValidator.validate_and_raise(value)
        super().__init__(value.strip().lower())
