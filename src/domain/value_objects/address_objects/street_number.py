from dataclasses import dataclass
from ..field import Field
from ...validators.number_validator import NumberValidator


@dataclass
class StreetNumber(Field):

    def __init__(self, value: int):
        if not isinstance(value, int):
            raise ValueError("StreetNumber must be a integer")
        if not NumberValidator.is_positive(value):
            raise ValueError("StreetNumber must be a positive integer")
        super().__init__(value)
