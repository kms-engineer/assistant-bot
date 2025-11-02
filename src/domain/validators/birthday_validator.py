import re
from datetime import datetime
from typing import Union
from src.config import DateFormatConfig, RegexPatterns, ValidationConfig
from .base_validator import BaseValidator


class BirthdayValidator(BaseValidator):

    _pattern = re.compile(RegexPatterns.BIRTHDAY_STRICT_PATTERN)

    @staticmethod
    def validate(birthday: str, date_format: str = None) -> Union[str, bool]:
        if date_format is None:
            date_format = DateFormatConfig.PRIMARY_DATE_FORMAT

        if not isinstance(birthday, str):
            return ValidationConfig.BIRTHDAY_ERROR_NOT_STRING

        if not birthday or len(birthday.strip()) == 0:
            return ValidationConfig.BIRTHDAY_ERROR_EMPTY

        if date_format == DateFormatConfig.PRIMARY_DATE_FORMAT:
            if not BirthdayValidator._pattern.fullmatch(birthday):
                return ValidationConfig.BIRTHDAY_ERROR_INVALID_FORMAT

        try:
            birthday_date = datetime.strptime(birthday, date_format)
            today = datetime.now()

            if birthday_date > today:
                return ValidationConfig.BIRTHDAY_ERROR_FUTURE_DATE

            if birthday_date.year < DateFormatConfig.MIN_BIRTHDAY_YEAR:
                return f"{ValidationConfig.BIRTHDAY_ERROR_INVALID_YEAR}: {birthday_date.year} (must be from {DateFormatConfig.MIN_BIRTHDAY_YEAR} onwards)"

            if not (1 <= birthday_date.month <= 12):
                return f"{ValidationConfig.BIRTHDAY_ERROR_INVALID_MONTH}: {birthday_date.month:02d}"

            return True
        except ValueError:
            return f"{ValidationConfig.BIRTHDAY_ERROR_INVALID_DATE}: {birthday}"
