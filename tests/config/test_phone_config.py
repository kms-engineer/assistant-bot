import pytest
from src.config.phone_config import PhoneConfig


class TestPhoneConfig:
    """Tests for the PhoneConfig class."""

    def test_exact_phone_length_is_int(self):
        """Test that EXACT_PHONE_LENGTH is a positive integer."""
        assert isinstance(PhoneConfig.EXACT_PHONE_LENGTH, int)
        assert PhoneConfig.EXACT_PHONE_LENGTH > 0
