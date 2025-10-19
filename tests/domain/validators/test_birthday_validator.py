import pytest
from datetime import datetime, timedelta
from src.domain.validators.birthday_validator import BirthdayValidator

# Based on the current date: Tuesday, October 14, 2025
TODAY = datetime.now().date()
CURRENT_YEAR = TODAY.year

@pytest.mark.parametrize("valid_birthday", [
    "15.06.1990",
    "29.02.2020",  # Leap year
    "01.01.1900",  # Boundary year
    TODAY.strftime("%d.%m.%Y"), # Today's date is valid
])
def test_validate_with_valid_birthday(valid_birthday):
    """Tests that a valid birthday string passes validation."""
    assert BirthdayValidator.validate(valid_birthday) is True

@pytest.mark.parametrize("invalid_input, expected_message", [
    (123, "Birthday must be a string"),
    (None, "Birthday must be a string"),
    (True, "Birthday must be a string"),
    ([], "Birthday must be a string"),
])
def test_validate_with_non_string_input(invalid_input, expected_message):
    """Tests that non-string inputs are rejected."""
    assert BirthdayValidator.validate(invalid_input) == expected_message

@pytest.mark.parametrize("empty_input", ["", "   ", "\t\n"])
def test_validate_with_empty_or_whitespace(empty_input):
    """Tests that empty or whitespace-only strings are rejected."""
    assert BirthdayValidator.validate(empty_input) == "Birthday cannot be empty or whitespace"

@pytest.mark.parametrize("bad_format_input", [
    "15-06-1990",
    "1990.06.15",
    "15.6.1990",
    "15.06.90",
    "fifteen.06.1990",
])
def test_validate_with_invalid_format(bad_format_input):
    """Tests strings that do not match the DD.MM.YYYY format."""
    assert BirthdayValidator.validate(bad_format_input) == "Birthday contain invalid date format. Use DD.MM.YYYY"

def test_validate_with_future_date():
    """Tests that a future date is rejected."""
    future_date = (TODAY + timedelta(days=1)).strftime("%d.%m.%Y")
    assert BirthdayValidator.validate(future_date) == "Birthday cannot be in future"

def test_validate_with_year_before_1900():
    """Tests that a year before 1900 is rejected."""
    assert BirthdayValidator.validate("31.12.1899") == "Birthday contain invalid year: 1899 (must be from 1900 onwards)"

@pytest.mark.parametrize("invalid_month_date", [
    "15.00.1995",
    "15.13.1995"
])
def test_validate_with_invalid_month(invalid_month_date):
    """Tests that a date with an invalid month is rejected."""
    assert BirthdayValidator.validate(invalid_month_date) == f"Birthday contain invalid date: {invalid_month_date}"

@pytest.mark.parametrize("invalid_day_date", [
    "31.04.2021", # April has 30 days
    "29.02.2021", # 2021 is not a leap year
    "32.01.2000", # January has 31 days
])
def test_validate_with_invalid_day(invalid_day_date):
    """Tests dates with a day that is invalid for the given month and year."""
    expected_message = f"Birthday contain invalid date: {invalid_day_date}"
    assert BirthdayValidator.validate(invalid_day_date) == expected_message
