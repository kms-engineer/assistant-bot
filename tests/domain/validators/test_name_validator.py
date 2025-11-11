import pytest
from src.domain.validators.name_validator import NameValidator
from src.config import ValidationConfig


class TestNameValidator:
    """Test suite for the NameValidator."""

    @pytest.mark.parametrize(
        "name",
        [
            "John",
            "John-Doe",
            "O'Malley",
            "J" * ValidationConfig.NAME_MIN_LENGTH,
            "J" * ValidationConfig.NAME_MAX_LENGTH,
        ],
        ids=[
            "simple_name",
            "hyphenated_name",
            "name_with_apostrophe",
            "min_length",
            "max_length",
        ],
    )
    def test_validate_success(self, name):
        """Scenario: A valid name string is provided."""
        assert NameValidator.validate(name) is True

    @pytest.mark.parametrize(
        "name, expected_error",
        [
            ("", ValidationConfig.NAME_ERROR_EMPTY),
            ("  ", ValidationConfig.NAME_ERROR_EMPTY),
            (None, ValidationConfig.NAME_ERROR_EMPTY),
            ("J", ValidationConfig.NAME_ERROR_TOO_SHORT),
            (
                "J" * (ValidationConfig.NAME_MAX_LENGTH + 1),
                ValidationConfig.NAME_ERROR_TOO_LONG,
            ),
            ("John123", ValidationConfig.NAME_ERROR_INVALID_CHARS),
            ("John!", ValidationConfig.NAME_ERROR_INVALID_CHARS),
        ],
        ids=[
            "empty_string",
            "whitespace_only",
            "none_value",
            "too_short",
            "too_long",
            "with_digits",
            "with_symbols",
        ],
    )
    def test_validate_failure(self, name, expected_error):
        """Scenario: An invalid name string is provided."""
        assert NameValidator.validate(name) == expected_error
