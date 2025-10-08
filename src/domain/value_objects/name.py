from dataclasses import dataclass
from ..validators.string_validator import StringValidator
from .field import Field


@dataclass
class Name(Field):

    def __init__(self, value: str):
        if not StringValidator.is_not_empty(value):
            raise ValueError("Name cannot be empty or whitespace.")
        super().__init__(value.strip())
