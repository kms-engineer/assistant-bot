from datetime import datetime, date


def parse_date(date_string: str, date_format: str) -> date:
    return datetime.strptime(date_string, date_format).date()


def get_next_birthday_date(orig_birthday: date, today: date) -> date:
    # get next year if birthday passed
    if orig_birthday.month > today.month or (orig_birthday.month == today.month and orig_birthday.day >= today.day):
        next_birthday_year = today.year
    else:
        next_birthday_year = today.year + 1

    try:
        return orig_birthday.replace(year=next_birthday_year)
    except ValueError:  # Feb 29 in non-leap year
        return date(next_birthday_year, 3, 1)
