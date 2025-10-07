from dataclasses import dataclass
from ..field import Field
from ...validators.string_validator import StringValidator


@dataclass
class State(Field):

    def __init__(self, value: str):
        if not isinstance(value, str):
            raise ValueError("State must be a string")
        if not StringValidator.is_not_empty(value):
            raise ValueError("State cannot be empty or whitespace.")
        super().__init__(value.strip())