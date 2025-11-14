from dataclasses import dataclass
from src.domain.validators.tag_validator import TagValidator
from src.domain.value_objects.field import Field


@dataclass
class Tag(Field):

    def __init__(self, value: str):
        TagValidator.validate_and_raise(value)
        super().__init__(value.strip())
