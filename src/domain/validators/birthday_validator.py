from datetime import datetime
from ..validators.string_validator import StringValidator

class BirthdayValidator:

    _pattern = r"\d{2}\.\d{2}\.\d{4}"

    @staticmethod
    def validate(birthday: str, date_format: str = "%d.%m.%Y") -> bool | str:
        if not StringValidator.is_string(birthday):
            return "Birthday must be a string"
        if not StringValidator.is_not_empty(birthday):
            return "Birthday cannot be empty or whitespace"
        if not StringValidator.exactly_match_pattern(birthday, BirthdayValidator._pattern):
            return "Birthday contain invalid date format. Use DD.MM.YYYY"

        try:
            birthday_date = datetime.strptime(birthday, "%d.%m.%Y")
            today = datetime.now()

            if birthday_date > today:
                return "Birthday cannot be in future"
            if birthday_date.year < 1900:
                return f"Birthday contain invalid year: {birthday_date.year} (must be from 1900 onwards)"
            if not (1 <= birthday_date.month <= 12):
                return f"Birthday contain invalid month: {birthday_date:02d}"
            return True
        except ValueError:
            return f"Birthday contain invalid date: {birthday}"
