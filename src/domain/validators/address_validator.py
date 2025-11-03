import re
from typing import Union

from src.config import ValidationConfig, RegexPatterns
from .base_validator import BaseValidator


class AddressValidator(BaseValidator):
    _ADDRESS_PATTERN = re.compile(RegexPatterns.VALIDATION_ADDRESS_PATTERN)
    _CITY_PATTERN = re.compile(RegexPatterns.ADDRESS_CITY_PATTERN)

    @staticmethod
    def validate(address: str) -> Union[str, bool]:
        if BaseValidator.is_empty_string(address):
            return ValidationConfig.ADDRESS_ERROR_EMPTY

        trimmed_address = address.strip()

        if len(trimmed_address) < ValidationConfig.ADDRESS_MIN_LENGTH:
            return ValidationConfig.ADDRESS_ERROR_TOO_SHORT

        if len(trimmed_address) > ValidationConfig.ADDRESS_MAX_LENGTH:
            return ValidationConfig.ADDRESS_ERROR_TOO_LONG

        if not AddressValidator._ADDRESS_PATTERN.fullmatch(trimmed_address):
            return ValidationConfig.ADDRESS_ERROR_INVALID_FORMAT

        return True
