import pytest
from src.domain.validators.address_validator import AddressValidator
from src.config import ValidationConfig


class TestAddressValidator:
    """Test suite for the AddressValidator."""

    @pytest.mark.parametrize(
        "address",
        [
            "123 Main St, Apt 4B",
            "Shevchenka St, 1, m. Lviv",
            "A" * ValidationConfig.ADDRESS_MIN_LENGTH,
            "A" * ValidationConfig.ADDRESS_MAX_LENGTH,
        ],
        ids=[
            "standard_address",
            "ukrainian_style_address",
            "min_length",
            "max_length",
        ]
    )
    def test_validate_success(self, address):
        """Scenario: A valid address string is provided."""
        assert AddressValidator.validate(address) is True

    @pytest.mark.parametrize(
        "address, expected_error",
        [
            ("", ValidationConfig.ADDRESS_ERROR_EMPTY),
            ("  ", ValidationConfig.ADDRESS_ERROR_EMPTY),
            (None, ValidationConfig.ADDRESS_ERROR_EMPTY),
            ("A", ValidationConfig.ADDRESS_ERROR_TOO_SHORT),
            ("A" * (ValidationConfig.ADDRESS_MAX_LENGTH + 1), ValidationConfig.ADDRESS_ERROR_TOO_LONG),
            ("123 Main St!", ValidationConfig.ADDRESS_ERROR_INVALID_FORMAT),
        ],
        ids=[
            "empty_string",
            "whitespace_only",
            "none_value",
            "too_short",
            "too_long",
            "invalid_character",
        ]
    )
    def test_validate_failure(self, address, expected_error):
        """Scenario: An invalid address string is provided."""
        assert AddressValidator.validate(address) == expected_error