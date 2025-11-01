import pytest
from src.config.validation_config import ValidationConfig


class TestValidationConfig:
    """Tests for the ValidationConfig class."""

    def test_length_configs_are_positive_integers(self):
        """Test that all length configurations are positive integers."""
        length_configs = [
            ValidationConfig.NAME_MIN_LENGTH,
            ValidationConfig.NAME_MAX_LENGTH,
            ValidationConfig.ADDRESS_MIN_LENGTH,
            ValidationConfig.ADDRESS_MAX_LENGTH,
            ValidationConfig.TAG_MAX_LENGTH,
            ValidationConfig.PHONE_MIN_DIGITS,
            ValidationConfig.PHONE_MAX_DIGITS,
        ]
        for config in length_configs:
            assert isinstance(config, int)
            assert config > 0

    def test_min_max_length_logic(self):
        """Test that min_length is less than or equal to max_length."""
        assert ValidationConfig.NAME_MIN_LENGTH <= ValidationConfig.NAME_MAX_LENGTH
        assert ValidationConfig.ADDRESS_MIN_LENGTH <= ValidationConfig.ADDRESS_MAX_LENGTH
        assert ValidationConfig.PHONE_MIN_DIGITS <= ValidationConfig.PHONE_MAX_DIGITS

    def test_error_messages_are_non_empty_strings(self):
        """Test that all error messages are non-empty strings."""
        for attr_name in dir(ValidationConfig):
            if attr_name.startswith("NAME_ERROR_") or \
               attr_name.startswith("EMAIL_ERROR_") or \
               attr_name.startswith("PHONE_ERROR_") or \
               attr_name.startswith("BIRTHDAY_ERROR_") or \
               attr_name.startswith("TAG_ERROR_") or \
               attr_name.startswith("ADDRESS_ERROR_") or \
               attr_name.startswith("NOTE_ERROR_"):
                error_message = getattr(ValidationConfig, attr_name)
                assert isinstance(error_message, str)
                assert error_message != ""
