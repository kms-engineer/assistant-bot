import pytest
from src.domain.validators.phone_validator import PhoneValidator
from src.config import ValidationConfig


class TestPhoneValidator:
    """Test suite for the PhoneValidator."""

    @pytest.mark.parametrize(
        "phone",
        [
            "1" * ValidationConfig.PHONE_MIN_DIGITS,
            "1" * ValidationConfig.PHONE_MAX_DIGITS,
            "+" + "1" * ValidationConfig.PHONE_MAX_DIGITS,
        ],
        ids=[
            "min_length",
            "max_length",
            "max_length_with_plus",
        ],
    )
    def test_validate_success(self, phone):
        """Scenario: A valid phone string is provided."""
        assert PhoneValidator.validate(phone) is True

    @pytest.mark.parametrize(
        "phone, expected_error",
        [
            (None, ValidationConfig.PHONE_ERROR_NOT_STRING),
            ("", ValidationConfig.PHONE_ERROR_EMPTY),
            ("1234567", ValidationConfig.PHONE_ERROR_INVALID_LENGTH),  # too short
            (
                "1" * (ValidationConfig.PHONE_MAX_DIGITS + 1),
                ValidationConfig.PHONE_ERROR_INVALID_LENGTH,
            ),  # too long
            ("123-456-7890", ValidationConfig.PHONE_ERROR_INVALID_FORMAT),
            ("123a4567890", ValidationConfig.PHONE_ERROR_INVALID_FORMAT),
            ("+123-456", ValidationConfig.PHONE_ERROR_INVALID_FORMAT),
        ],
        ids=[
            "none_value",
            "empty_string",
            "too_short",
            "too_long",
            "with_hyphens",
            "with_letters",
            "plus_with_hyphens",
        ],
    )
    def test_validate_failure(self, phone, expected_error):
        """Scenario: An invalid phone string is provided."""
        assert PhoneValidator.validate(phone) == expected_error

    @pytest.mark.parametrize(
        "raw_phone, expected_normalized",
        [
            ("+1 (234) 567-8900", "12345678900"),
            ("123-456-7890", "1234567890"),
            ("1234567890", "1234567890"),
            ("", ""),
            (None, ""),
        ],
        ids=[
            "full_format_with_plus",
            "hyphenated_format",
            "digits_only",
            "empty_string",
            "none_value",
        ],
    )
    def test_normalize(self, raw_phone, expected_normalized):
        """
        Scenario: Various raw phone strings are provided to the normalize method.
        Expected: The method should return a string containing only the digits.
        """
        assert PhoneValidator.normalize(raw_phone) == expected_normalized
