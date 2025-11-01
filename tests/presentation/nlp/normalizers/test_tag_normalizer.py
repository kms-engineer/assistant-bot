import pytest
from src.presentation.nlp.normalizers.tag_normalizer import TagNormalizer


class TestTagNormalizer:
    """
    Test suite for the TagNormalizer.
    Verifies that tags are correctly prefixed with '#' and that invalid
    characters are stripped out.
    """

    @pytest.mark.parametrize(
        "input_tag, expected_tag",
        [
            # Scenario: Tag without prefix
            ("python", "#python"),
            # Scenario: Tag with existing prefix
            ("#django", "#django"),
            # Scenario: Tag with invalid characters
            ("c++_programming!", "#c_programming"),
            # Scenario: Tag with spaces and prefix needed
            (" web dev ", "#webdev"),
            # Scenario: Tag with mixed valid and invalid characters
            ("#data-science?", "#datascience"),
        ],
        ids=[
            "add_prefix",
            "existing_prefix",
            "invalid_chars",
            "spaces_and_prefix",
            "mixed_chars",
        ]
    )
    def test_normalize(self, input_tag, expected_tag):
        """Tests the normalize method with various tag formats."""
        entities = {"tag": input_tag}
        result = TagNormalizer.normalize(entities)
        assert result['tag'] == expected_tag

    def test_normalize_no_tag_key(self):
        """Tests that the normalizer does nothing if the 'tag' key is missing."""
        entities = {"note_text": "some text"}
        result = TagNormalizer.normalize(entities.copy())
        assert result == entities