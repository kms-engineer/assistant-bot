import re
from datetime import datetime


class BirthdayValidator:

    @staticmethod
    def validate(birthday: str) -> bool:
        if not re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", birthday):
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

        day, month, year = map(int, birthday.split('.'))
        current_year = datetime.now().year

        if year > current_year:
            raise ValueError("Birthday cannot be in future")
        if year < 1900:
            raise ValueError(f"Invalid year: {year} (must be from 1900 onwards)")
        if not (1 <= month <= 12):
            raise ValueError(f"Invalid month: {month:02d}")

        try:
            datetime.strptime(birthday, "%d.%m.%Y")
            return True
        except ValueError:
            raise(f"Invalid day: {day:02d} for month {month:02d}/{year}")
