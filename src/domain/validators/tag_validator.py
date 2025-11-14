from typing import Union
from src.config import ValidationConfig
from src.domain.validators.base_validator import BaseValidator


class TagValidator(BaseValidator):

    @staticmethod
    def validate(value: str) -> Union[str, bool]:
        if not isinstance(value, str):
            return ValidationConfig.TAG_ERROR_NOT_STRING

        if not value or len(value.strip()) == 0:
            return ValidationConfig.TAG_ERROR_EMPTY

        if len(value) > ValidationConfig.TAG_MAX_LENGTH:
            return ValidationConfig.TAG_ERROR_TOO_LONG

        return True
