import pytest
from src.domain.value_objects.birthday import Birthday
from datetime import datetime


@pytest.mark.parametrize(
    "valid_birthday",
    [
        "15.06.1990",
        "29.02.2024",  # Valid leap year
        "01.01.1900",  # Boundary year
    ],
)
def test_birthday_creation_with_valid_date(valid_birthday):
    """Tests that a Birthday object is created successfully with a valid date."""
    birthday_obj = Birthday(valid_birthday)
    assert birthday_obj.value == valid_birthday


@pytest.mark.parametrize(
    "invalid_input, expected_error_message",
    [
        # Type and presence checks
        (12345, "Birthday must be a string"),
        (None, "Birthday must be a string"),
        ("", "Birthday cannot be empty or whitespace"),
        ("   ", "Birthday cannot be empty or whitespace"),
        # Format checks
        ("15-06-1990", "Birthday contain invalid date format. Use DD.MM.YYYY"),
        ("1990.06.15", "Birthday contain invalid date format. Use DD.MM.YYYY"),
        ("15.6.1990", "Birthday contain invalid date format. Use DD.MM.YYYY"),
        # Logical date checks
        (f"01.01.{datetime.now().year + 1}", "Birthday cannot be in future"),
        (
            "15.06.1899",
            "Birthday contain invalid year: 1899 (must be from 1900 onwards)",
        ),
        ("15.13.2000", "Birthday contain invalid date: 15.13.2000"),
        ("31.04.2023", "Birthday contain invalid date: 31.04.2023"),
        ("29.02.2023", "Birthday contain invalid date: 29.02.2023"),  # Invalid leap day
    ],
)
def test_birthday_creation_with_invalid_date(invalid_input, expected_error_message):
    """
    Tests that creating a Birthday with invalid input raises a ValueError
    with the correct message from the validator.
    """
    with pytest.raises(ValueError) as excinfo:
        Birthday(invalid_input)
    assert str(excinfo.value) == expected_error_message
