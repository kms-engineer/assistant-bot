import pytest
from datetime import date
from src.domain.utils.birthday_utils import parse_date, get_next_birthday_date


class TestBirthdayUtils:
    """Tests for the birthday utility functions."""

    def test_parse_date_success(self):
        """Test successful parsing of a valid date string."""
        date_string = "25.12.2023"
        date_format = "%d.%m.%Y"
        expected_date = date(2023, 12, 25)
        assert parse_date(date_string, date_format) == expected_date

    def test_parse_date_invalid_format(self):
        """Test that parsing an invalid date string raises ValueError."""
        date_string = "2023-12-25"
        date_format = "%d.%m.%Y"
        with pytest.raises(ValueError):
            parse_date(date_string, date_format)

    def test_get_next_birthday_date_before_birthday(self):
        """Test when the birthday for the current year has not occurred yet."""
        today = date(2023, 1, 1)
        birthday = date(1990, 10, 25)
        expected = date(2023, 10, 25)
        assert get_next_birthday_date(birthday, today) == expected

    def test_get_next_birthday_date_after_birthday(self):
        """Test when the birthday for the current year has already passed."""
        today = date(2023, 11, 1)
        birthday = date(1990, 10, 25)
        expected = date(2024, 10, 25)
        assert get_next_birthday_date(birthday, today) == expected

    def test_get_next_birthday_date_on_birthday(self):
        """Test when today is the person's birthday."""
        today = date(2023, 10, 25)
        birthday = date(1990, 10, 25)
        expected = date(2023, 10, 25)
        assert get_next_birthday_date(birthday, today) == expected

    def test_get_next_birthday_leap_year_birthday(self):
        """Test handling of a birthday on February 29th."""
        birthday = date(2000, 2, 29)
        # Case 1: Next birthday is in a non-leap year
        today_non_leap = date(2023, 1, 1)
        expected_non_leap = date(2023, 3, 1)
        assert get_next_birthday_date(birthday, today_non_leap) == expected_non_leap
        # Case 2: Next birthday is in a leap year
        today_leap = date(2024, 1, 1)
        expected_leap = date(2024, 2, 29)
        assert get_next_birthday_date(birthday, today_leap) == expected_leap
