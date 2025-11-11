import pytest
from src.domain.validators.note_text_validator import NoteTextValidator
from src.config import ValidationConfig


class TestNoteTextValidator:
    """Test suite for the NoteTextValidator."""

    @pytest.mark.parametrize(
        "text",
        [
            "This is a note.",
            "a",
            "  This is a note with whitespace.  ",
        ],
        ids=["simple_note", "single_character", "with_whitespace"],
    )
    def test_validate_success(self, text):
        """Scenario: Valid note text is provided."""
        assert NoteTextValidator.validate(text) is True

    @pytest.mark.parametrize(
        "text, expected_error",
        [
            (None, ValidationConfig.NOTE_ERROR_NOT_STRING),
            ("", ValidationConfig.NOTE_ERROR_EMPTY),
            ("   ", ValidationConfig.NOTE_ERROR_EMPTY),
        ],
        ids=["none_value", "empty_string", "whitespace_only"],
    )
    def test_validate_failure(self, text, expected_error):
        """Scenario: Invalid note text is provided."""
        assert NoteTextValidator.validate(text) == expected_error
