from dataclasses import dataclass
from ..field import Field
from ...validators.string_validator import StringValidator


@dataclass
class Country(Field):

    def __init__(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Country must be a string")
        if not StringValidator.is_not_empty(value):
            raise ValueError("Country cannot be empty or whitespace.")
        super().__init__(value.strip())
