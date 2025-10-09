from datetime import timedelta, date


def get_birthday_for_year(orig_birthday: date, target_year: int) -> date:
    try:
        return orig_birthday.replace(year=target_year)
    except ValueError:  # Feb 29 in non-leap year
        return date(target_year, 3, 1)


def move_to_monday_if_weekend(input_date: date) -> date:
    weekday = input_date.weekday()
    if weekday >= 5:  # Weekend (5=Saturday, 6=Sunday)
        return input_date + timedelta(days=(7 - weekday))
    return input_date
