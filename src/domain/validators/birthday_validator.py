from datetime import datetime
from ..validators.string_validator import StringValidator

class BirthdayValidator:

    _pattern = r"\d{2}\.\d{2}\.\d{4}"

    @staticmethod
    def validate(birthday: str) -> bool | str:
        if not StringValidator.is_string(birthday):
            return "Birthday must be a string"
        if not StringValidator.is_not_empty(birthday):
            return "Birthday cannot be empty or whitespace"
        if not StringValidator.exactly_match_pattern(birthday, BirthdayValidator._pattern):
            return "Birthday contain invalid date format. Use DD.MM.YYYY"

        day, month, year = map(int, birthday.split('.'))
        current_year = datetime.now().year

        if year > current_year:
            return "Birthday cannot be in future"
        if year < 1900:
            return f"Birthday contain invalid year: {year} (must be from 1900 onwards)"
        if not (1 <= month <= 12):
            return f"Birthday contain invalid month: {month:02d}"

        try:
            datetime.strptime(birthday, "%d.%m.%Y")
            return True
        except ValueError:
            return f"Birthday contain invalid day: {day:02d} for month {month:02d}/{year}"
