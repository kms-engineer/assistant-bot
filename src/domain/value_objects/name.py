from dataclasses import dataclass
from ..validators.name_validator import NameValidator
from .field import Field


@dataclass
class Name(Field):

    def __init__(self, value: str):
        validation_result = NameValidator.validate(value)
        if validation_result is not True:
            raise ValueError(str(validation_result))
        super().__init__(value.strip())
