import pytest
from unittest.mock import patch
from src.presentation.nlp.normalizers.email_normalizer import EmailNormalizer


class TestEmailNormalizer:
    """
    Test suite for the EmailNormalizer.
    Verifies email validation and normalization, including the graceful
    fallback when the optional 'email_validator' library is not present.
    """

    @pytest.mark.parametrize(
        "input_email, expected_normalized, validator_available",
        [
            # Scenario: With email-validator, simple case
            ("test@example.com", "test@example.com", True),
            # Scenario: With email-validator, needs normalization (uppercase)
            ("Test.User@EXAMPLE.COM", "test.user@example.com", True),
            # Scenario: Without email-validator, simple case
            ("test@example.com", "test@example.com", False),
            # Scenario: Without email-validator, needs normalization (strip and lower)
            ("  Test@Example.com  ", "test@example.com", False),
        ],
        ids=[
            "validator_simple",
            "validator_normalization",
            "no_validator_simple",
            "no_validator_normalization",
        ],
    )
    def test_normalize_valid_email(
        self, input_email, expected_normalized, validator_available
    ):
        """Tests normalization of valid email strings."""
        with patch(
            "src.presentation.nlp.normalizers.email_normalizer.EMAIL_VALIDATOR_AVAILABLE",
            validator_available,
        ):
            entities = {"email": input_email}
            result = EmailNormalizer.normalize(entities)

            assert result["_email_valid"] is True
            assert result["email"] == expected_normalized

    @pytest.mark.parametrize(
        "invalid_email, validator_available",
        [
            # Scenario: Invalid format (missing @)
            ("test.example.com", True),
            ("test.example.com", False),
            # Scenario: Invalid format (missing domain)
            ("test@", True),
            ("test@", False),
        ],
        ids=[
            "validator_invalid_no_at",
            "no_validator_invalid_no_at",
            "validator_invalid_no_domain",
            "no_validator_invalid_no_domain",
        ],
    )
    def test_normalize_invalid_email(self, invalid_email, validator_available):
        """Tests handling of invalid email strings."""
        with patch(
            "src.presentation.nlp.normalizers.email_normalizer.EMAIL_VALIDATOR_AVAILABLE",
            validator_available,
        ):
            entities = {"email": invalid_email}
            result = EmailNormalizer.normalize(entities)

            assert result["_email_valid"] is False
            assert "_validation_errors" in result
            assert len(result["_validation_errors"]) > 0

    def test_normalize_no_email_key(self):
        """Tests that the normalizer does nothing if the 'email' key is missing."""
        entities = {"name": "John"}
        result = EmailNormalizer.normalize(entities.copy())
        assert result == entities

    def test_normalize_empty_email(self):
        """Tests that the normalizer does nothing if the 'email' value is empty."""
        entities = {"email": ""}
        result = EmailNormalizer.normalize(entities.copy())
        assert result == entities
