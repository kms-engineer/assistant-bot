import pytest
from src.domain.value_objects.phone import Phone

@pytest.mark.parametrize("raw_phone_input, expected_digits", [
    ("1234567890", "1234567890"),
    ("(123) 456-7890", "1234567890"),
    ("123.456.7890", "1234567890"),
    (" 123 456 7890 ", "1234567890"),
])
def test_phone_creation_with_valid_number(raw_phone_input, expected_digits):
    """
    Tests that a Phone object is created successfully with various valid
    raw phone number formats, normalizing them correctly.
    """
    phone_obj = Phone(raw_phone_input)
    assert phone_obj.value == expected_digits

@pytest.mark.parametrize("invalid_raw_input, expected_error_message", [
    ("12345", "Phone number must be exactly 10 digits long"),
    ("123-456-789", "Phone number must be exactly 10 digits long"),
    ("12345678901", "Phone number must be exactly 10 digits long"),
    ("(123) 456-7890 Ext 1", "Phone number must be exactly 10 digits long"),
    ("not a number", "Phone number must be exactly 10 digits long"), # Normalizes to ""
    ("", "Phone number must be exactly 10 digits long"),
])
def test_phone_creation_with_invalid_length(invalid_raw_input, expected_error_message):
    """
    Tests that creating a Phone with a raw string that normalizes to an
    incorrect length raises a ValueError.
    """
    with pytest.raises(ValueError) as excinfo:
        Phone(invalid_raw_input)
    assert str(excinfo.value) == expected_error_message

@pytest.mark.parametrize("non_string_input", [
    1234567890,
    None,
    [],
])
def test_phone_creation_with_non_string_input(non_string_input):
    """
    Tests that creating a Phone with a non-string input raises a TypeError
    when normalization is attempted.
    """
    with pytest.raises(TypeError):
        Phone(non_string_input)
