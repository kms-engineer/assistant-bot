from dataclasses import dataclass
from ..validators.tag_validator import TagValidator
from .field import Field


@dataclass
class Tag(Field):

    def __init__(self, value: str):
        validation_result = TagValidator.validate(value)
        if validation_result is not True:
            raise ValueError(str(validation_result))
        super().__init__(value.strip())
