from dataclasses import dataclass
from src.domain.validators.email_validator import EmailValidator
from src.domain.value_objects.field import Field


@dataclass
class Email(Field):

    def __init__(self, value: str):
        EmailValidator.validate_and_raise(value)
        super().__init__(value.strip().lower())
