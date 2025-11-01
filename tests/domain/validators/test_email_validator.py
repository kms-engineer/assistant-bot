import pytest
from src.domain.validators.email_validator import EmailValidator
from src.config import ValidationConfig


class TestEmailValidator:
    """Test suite for the EmailValidator."""

    @pytest.mark.parametrize(
        "email",
        [
            "test@example.com",
            "test.name@example.co.uk",
            "test-name@example.com",
            "123@example.com",
            "  test@example.com  ",  # Should be trimmed
        ],
        ids=[
            "simple_email",
            "subdomain_email",
            "hyphen_email",
            "numeric_local_part",
            "with_whitespace",
        ]
    )
    def test_validate_success(self, email):
        """Scenario: A valid email string is provided."""
        assert EmailValidator.validate(email) is True

    @pytest.mark.parametrize(
        "email, expected_error",
        [
            ("", ValidationConfig.EMAIL_ERROR_EMPTY),
            ("  ", ValidationConfig.EMAIL_ERROR_EMPTY),
            (None, ValidationConfig.EMAIL_ERROR_EMPTY),
            ("test", ValidationConfig.EMAIL_ERROR_INVALID_FORMAT),
            ("test@", ValidationConfig.EMAIL_ERROR_INVALID_FORMAT),
            ("@example.com", ValidationConfig.EMAIL_ERROR_INVALID_FORMAT),
            ("test@.com", ValidationConfig.EMAIL_ERROR_INVALID_FORMAT),
            ("test@example..com", ValidationConfig.EMAIL_ERROR_INVALID_FORMAT),
            ("a" * (ValidationConfig.EMAIL_MAX_LENGTH) + "@test.com", ValidationConfig.EMAIL_ERROR_TOO_LONG),
        ],
        ids=[
            "empty_string",
            "whitespace_only",
            "none_value",
            "no_at_symbol",
            "no_domain",
            "no_local_part",
            "no_domain_name",
            "double_dot_in_domain",
            "too_long",
        ]
    )
    def test_validate_failure(self, email, expected_error):
        """Scenario: An invalid email string is provided."""
        assert EmailValidator.validate(email) == expected_error