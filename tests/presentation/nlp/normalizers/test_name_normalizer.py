import pytest
from src.presentation.nlp.normalizers.name_normalizer import NameNormalizer


class TestNameNormalizer:
    """
    Test suite for the NameNormalizer.
    Verifies that names are correctly capitalized, stripped of extra whitespace,
    and validated for minimum length.
    """

    @pytest.mark.parametrize(
        "input_name, expected_name",
        [
            # Scenario: Simple name, all lowercase
            ("john doe", "John Doe"),
            # Scenario: Name with extra whitespace
            ("  jane   roe  ", "Jane Roe"),
            # Scenario: Already capitalized name
            ("Richard Roe", "Richard Roe"),
            # Scenario: Mixed case name
            ("pEtEr jOnEs", "Peter Jones"),
            # Scenario: Single word name
            ("cher", "Cher"),
        ],
        ids=[
            "simple_lowercase",
            "extra_whitespace",
            "already_capitalized",
            "mixed_case",
            "single_word",
        ],
    )
    def test_normalize_valid_name(self, input_name, expected_name):
        """Tests normalization of valid name strings."""
        entities = {"name": input_name}
        result = NameNormalizer.normalize(entities)
        assert result["name"] == expected_name
        assert result["_name_valid"] is True

    def test_normalize_name_too_short(self):
        """Tests that a name shorter than 2 characters is marked as invalid."""
        entities = {"name": "a"}
        result = NameNormalizer.normalize(entities)
        assert result["name"] == "A"
        assert result["_name_valid"] is False
        assert "_validation_errors" in result
        assert "Name too short: A" in result["_validation_errors"]

    def test_normalize_no_name_key(self):
        """Tests that the normalizer does nothing if the 'name' key is missing."""
        entities = {"email": "test@test.com"}
        result = NameNormalizer.normalize(entities.copy())
        assert result == entities
