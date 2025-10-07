from dataclasses import dataclass
from ..validators.email_validator import EmailValidator
from .field import Field


@dataclass
class Email(Field):

    def __init__(self, value: str):
        validation_result = EmailValidator.validate(value)
        if validation_result is not True:
            raise ValueError(str(validation_result))
        super().__init__(value)
