from dataclasses import dataclass
from ..validators.tag_validator import TagValidator
from .field import Field


@dataclass
class Tag(Field):

    def __init__(self, value: str):
        TagValidator.validate(value)
        super().__init__(value.strip())
