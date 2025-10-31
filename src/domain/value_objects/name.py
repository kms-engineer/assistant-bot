from dataclasses import dataclass
from ..validators.name_validator import NameValidator
from .field import Field


@dataclass
class Name(Field):

    def __init__(self, value: str):
        NameValidator.validate_and_raise(value)
        super().__init__(value.strip())
