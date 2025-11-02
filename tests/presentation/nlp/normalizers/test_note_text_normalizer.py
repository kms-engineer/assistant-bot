import pytest
from src.presentation.nlp.normalizers.note_text_normalizer import NoteTextNormalizer


class TestNoteTextNormalizer:
    """
    Test suite for the NoteTextNormalizer.
    Verifies that note text is cleaned by removing extra whitespace and
    surrounding quotation marks.
    """

    @pytest.mark.parametrize(
        "input_text, expected_text",
        [
            # Scenario: Text with extra whitespace
            ("  This is   a note.  ", "This is a note."),
            # Scenario: Text surrounded by single quotes
            ("'This is a quoted note.'", "This is a quoted note."),
            # Scenario: Text surrounded by double quotes
            ('"This is another quoted note."', "This is another quoted note."),
            # Scenario: Text with internal quotes (should be preserved)
            ("He said 'hello' to me.", "He said 'hello' to me."),
            # Scenario: Clean text (should remain unchanged)
            ("A simple note.", "A simple note."),
        ],
        ids=[
            "extra_whitespace",
            "single_quotes",
            "double_quotes",
            "internal_quotes",
            "clean_text",
        ]
    )
    def test_normalize(self, input_text, expected_text):
        """Tests the normalize method with various text formats."""
        entities = {"note_text": input_text}
        result = NoteTextNormalizer.normalize(entities)
        assert result['note_text'] == expected_text