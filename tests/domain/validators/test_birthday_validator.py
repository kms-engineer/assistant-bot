import pytest
from datetime import datetime, timedelta
from src.domain.validators.birthday_validator import BirthdayValidator
from src.config import ValidationConfig, DateFormatConfig


class TestBirthdayValidator:
    """Test suite for the BirthdayValidator."""

    def test_validate_success(self):
        """Scenario: A valid birthday string is provided."""
        assert BirthdayValidator.validate("25.12.1990") is True

    @pytest.mark.parametrize(
        "birthday, expected_error_part",
        [
            (None, ValidationConfig.BIRTHDAY_ERROR_NOT_STRING),
            ("", ValidationConfig.BIRTHDAY_ERROR_EMPTY),
            ("  ", ValidationConfig.BIRTHDAY_ERROR_EMPTY),
            ("25-12-1990", ValidationConfig.BIRTHDAY_ERROR_INVALID_FORMAT),
            ("1990.12.25", ValidationConfig.BIRTHDAY_ERROR_INVALID_FORMAT),
            ("32.12.1990", ValidationConfig.BIRTHDAY_ERROR_INVALID_DATE),  # Invalid day
            (
                "25.13.1990",
                ValidationConfig.BIRTHDAY_ERROR_INVALID_DATE,
            ),  # Invalid month
            (
                "29.02.1991",
                ValidationConfig.BIRTHDAY_ERROR_INVALID_DATE,
            ),  # Not a leap year
            (
                (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y"),
                ValidationConfig.BIRTHDAY_ERROR_FUTURE_DATE,
            ),
            (
                f"01.01.{DateFormatConfig.MIN_BIRTHDAY_YEAR - 1}",
                ValidationConfig.BIRTHDAY_ERROR_INVALID_YEAR,
            ),
        ],
        ids=[
            "none_value",
            "empty_string",
            "whitespace_only",
            "wrong_delimiter",
            "wrong_format",
            "invalid_day",
            "invalid_month",
            "invalid_leap_day",
            "future_date",
            "year_too_early",
        ],
    )
    def test_validate_failure(self, birthday, expected_error_part):
        """Scenario: An invalid birthday string is provided."""
        result = BirthdayValidator.validate(birthday)
        assert isinstance(result, str)
        assert expected_error_part in result

    def test_validate_success_leap_year(self):
        """Scenario: A valid leap day birthday is provided."""
        assert BirthdayValidator.validate("29.02.2000") is True

    def test_validate_custom_format(self):
        """
        Scenario: A custom date format is provided to the validator.
        Expected: Validation succeeds for the custom format and fails for the default.
        """
        custom_format = "%Y-%m-%d"
        valid_date = "2000-01-25"
        invalid_date_for_custom = "25.01.2000"

        assert BirthdayValidator.validate(valid_date, date_format=custom_format) is True
        assert (
            BirthdayValidator.validate(
                invalid_date_for_custom, date_format=custom_format
            )
            is not True
        )
