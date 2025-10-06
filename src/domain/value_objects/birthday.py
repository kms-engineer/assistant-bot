from ..validators.birthday_validator import BirthdayValidator
from .field import Field


class Birthday(Field):

    def __init__(self, value: str):
        validation_result = BirthdayValidator.validate(value)
        if validation_result is not True:
            raise ValueError(str(validation_result))
        super().__init__(value)
