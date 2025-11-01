import pytest
from src.config.date_format_config import DateFormatConfig
import datetime


class TestDateFormatConfig:
    """Tests for the DateFormatConfig class."""

    def test_primary_date_format_is_valid(self):
        """Test that PRIMARY_DATE_FORMAT is a valid format string."""
        assert isinstance(DateFormatConfig.PRIMARY_DATE_FORMAT, str)
        try:
            datetime.datetime.now().strftime(DateFormatConfig.PRIMARY_DATE_FORMAT)
        except ValueError:
            pytest.fail(f"PRIMARY_DATE_FORMAT '{DateFormatConfig.PRIMARY_DATE_FORMAT}' is not a valid format string.")

    def test_min_birthday_year_is_int(self):
        """Test that MIN_BIRTHDAY_YEAR is a reasonable integer."""
        assert isinstance(DateFormatConfig.MIN_BIRTHDAY_YEAR, int)
        assert 1800 <= DateFormatConfig.MIN_BIRTHDAY_YEAR < datetime.datetime.now().year
