from dataclasses import dataclass
from src.domain.validators.name_validator import NameValidator
from src.domain.value_objects.field import Field


@dataclass
class Name(Field):

    def __init__(self, value: str):
        NameValidator.validate_and_raise(value)
        super().__init__(value.strip())
