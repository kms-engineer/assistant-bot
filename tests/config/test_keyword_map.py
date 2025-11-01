import pytest
from src.config.keyword_map import KEYWORD_MAP, GREETING_KEYWORDS


class TestKeywordMap:
    """Tests for the keyword map configurations."""

    def test_keyword_map_structure(self):
        """Test that KEYWORD_MAP is a dictionary of lists of strings."""
        assert isinstance(KEYWORD_MAP, dict)
        for key, value in KEYWORD_MAP.items():
            assert isinstance(key, str)
            assert isinstance(value, list)
            for item in value:
                assert isinstance(item, str)

    def test_greeting_keywords_structure(self):
        """Test that GREETING_KEYWORDS is a list of strings."""
        assert isinstance(GREETING_KEYWORDS, list)
        for item in GREETING_KEYWORDS:
            assert isinstance(item, str)

    def test_no_empty_keywords(self):
        """Test that there are no empty strings in the keyword lists."""
        for key, value in KEYWORD_MAP.items():
            for item in value:
                assert item.strip() != "", f"Empty keyword found in {key}"
        for item in GREETING_KEYWORDS:
            assert item.strip() != "", "Empty keyword found in GREETING_KEYWORDS"
