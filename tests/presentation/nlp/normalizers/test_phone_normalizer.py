import pytest
from unittest.mock import patch
from src.presentation.nlp.normalizers.phone_normalizer import PhoneNormalizer


class TestPhoneNormalizer:
    """
    Test suite for the PhoneNormalizer.
    Verifies phone number parsing and formatting, including the critical
    handling of the optional 'phonenumbers' library.
    """

    @pytest.mark.parametrize(
        "input_phone, region, expected_e164, expected_national",
        [
            # Scenario: International format
            ("+12125552368", "US", "+12125552368", "(212) 555-2368"),
            # Scenario: National format (US)
            ("(415) 555-2671", "US", "+14155552671", "(415) 555-2671"),
            # Scenario: National format (GB)
            ("020 7946 0000", "GB", "+442079460000", "020 7946 0000"),
        ],
        ids=["international_format", "us_national_format", "gb_national_format"],
    )
    def test_normalize_valid_phone_with_library(
        self, input_phone, region, expected_e164, expected_national
    ):
        """Tests normalization of valid phone numbers when 'phonenumbers' is available."""
        with patch(
            "src.presentation.nlp.normalizers.phone_normalizer.PHONENUMBERS_AVAILABLE",
            True,
        ):
            entities = {"phone": input_phone}
            result = PhoneNormalizer.normalize(entities, default_region=region)

            assert result["_phone_valid"] is True
            assert result["phone"] == expected_e164
            assert result["phone_national"] == expected_national

    def test_normalize_invalid_phone_with_library(self):
        """Tests handling of an invalid phone number when 'phonenumbers' is available."""
        with patch(
            "src.presentation.nlp.normalizers.phone_normalizer.PHONENUMBERS_AVAILABLE",
            True,
        ):
            entities = {"phone": "123"}
            result = PhoneNormalizer.normalize(entities, default_region="US")

            assert result["_phone_valid"] is False
            assert "_validation_errors" in result
            assert "Invalid phone number: 123" in result["_validation_errors"]

    def test_normalize_without_library(self):
        """Tests that normalization fails gracefully when 'phonenumbers' is not available."""
        with patch(
            "src.presentation.nlp.normalizers.phone_normalizer.PHONENUMBERS_AVAILABLE",
            False,
        ):
            entities = {"phone": "+12125552368"}
            result = PhoneNormalizer.normalize(entities)

            assert result["_phone_valid"] is False
            assert "_validation_errors" in result
            assert "phonenumbers library not available" in result["_validation_errors"]

    def test_normalize_no_phone_key(self):
        """Tests that the normalizer does nothing if the 'phone' key is missing."""
        entities = {"name": "John"}
        result = PhoneNormalizer.normalize(entities.copy())
        assert result == entities

    def test_normalize_empty_phone(self):
        """Tests that the normalizer does nothing if the 'phone' value is empty."""
        entities = {"phone": ""}
        result = PhoneNormalizer.normalize(entities.copy())
        assert result == entities
