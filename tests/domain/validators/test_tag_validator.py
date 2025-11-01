import pytest
from src.domain.validators.tag_validator import TagValidator
from src.config import ValidationConfig


class TestTagValidator:
    """Test suite for the TagValidator."""

    @pytest.mark.parametrize(
        "tag",
        [
            "python",
            "a",
            "a" * ValidationConfig.TAG_MAX_LENGTH,
        ],
        ids=[
            "simple_tag",
            "min_length_implied",
            "max_length",
        ]
    )
    def test_validate_success(self, tag):
        """Scenario: A valid tag string is provided."""
        assert TagValidator.validate(tag) is True

    @pytest.mark.parametrize(
        "tag, expected_error",
        [
            (None, ValidationConfig.TAG_ERROR_NOT_STRING),
            (123, ValidationConfig.TAG_ERROR_NOT_STRING),
            ("", ValidationConfig.TAG_ERROR_EMPTY),
            ("  ", ValidationConfig.TAG_ERROR_EMPTY),
            ("a" * (ValidationConfig.TAG_MAX_LENGTH + 1), ValidationConfig.TAG_ERROR_TOO_LONG),
        ],
        ids=["none_value", "not_a_string", "empty_string", "whitespace_only", "too_long"]
    )
    def test_validate_failure(self, tag, expected_error):
        """Scenario: An invalid tag is provided."""
        assert TagValidator.validate(tag) == expected_error