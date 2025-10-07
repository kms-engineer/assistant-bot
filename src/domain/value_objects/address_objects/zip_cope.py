from dataclasses import dataclass
from ..field import Field
from ...validators.number_validator import NumberValidator


@dataclass
class ZipCode(Field):

    def __init__(self, value: int):
        if not isinstance(value, int):
            raise ValueError("ZipCode must be a integer")
        if not NumberValidator.is_positive(value):
            raise ValueError("ZipCode must be a positive integer")
        super().__init__(value)
