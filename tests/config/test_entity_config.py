import pytest
from src.config.entity_config import EntityConfig


class TestEntityConfig:
    """Tests for the EntityConfig class."""

    def test_entity_labels_structure(self):
        """Test that ENTITY_LABELS is a list of strings."""
        assert isinstance(EntityConfig.ENTITY_LABELS, list)
        for label in EntityConfig.ENTITY_LABELS:
            assert isinstance(label, str)

    def test_regex_preferred_fields_structure(self):
        """Test that REGEX_PREFERRED_FIELDS is a set of strings."""
        assert isinstance(EntityConfig.REGEX_PREFERRED_FIELDS, set)
        for field in EntityConfig.REGEX_PREFERRED_FIELDS:
            assert isinstance(field, str)

    def test_ner_preferred_fields_structure(self):
        """Test that NER_PREFERRED_FIELDS is a set of strings."""
        assert isinstance(EntityConfig.NER_PREFERRED_FIELDS, set)
        for field in EntityConfig.NER_PREFERRED_FIELDS:
            assert isinstance(field, str)

    def test_default_confidence_values(self):
        """Test the values and types of default confidence scores."""
        assert isinstance(EntityConfig.DEFAULT_REGEX_CONFIDENCE, float)
        assert 0.0 <= EntityConfig.DEFAULT_REGEX_CONFIDENCE <= 1.0
        assert isinstance(EntityConfig.DEFAULT_REGEX_NO_MATCH_CONFIDENCE, float)
        assert 0.0 <= EntityConfig.DEFAULT_REGEX_NO_MATCH_CONFIDENCE <= 1.0
        assert isinstance(EntityConfig.DEFAULT_NER_CONFIDENCE, float)
        assert 0.0 <= EntityConfig.DEFAULT_NER_CONFIDENCE <= 1.0
        assert isinstance(EntityConfig.DEFAULT_NER_NO_MATCH_CONFIDENCE, float)
        assert 0.0 <= EntityConfig.DEFAULT_NER_NO_MATCH_CONFIDENCE <= 1.0
        assert isinstance(EntityConfig.ENTITY_MERGE_THRESHOLD, float)
        assert 0.0 <= EntityConfig.ENTITY_MERGE_THRESHOLD <= 1.0
        assert isinstance(EntityConfig.DEFAULT_ENTITY_CONFIDENCE, float)
        assert 0.0 <= EntityConfig.DEFAULT_ENTITY_CONFIDENCE <= 1.0

    def test_stop_words_structure(self):
        """Test that STOP_WORDS is a set of strings."""
        assert isinstance(EntityConfig.STOP_WORDS, set)
        for word in EntityConfig.STOP_WORDS:
            assert isinstance(word, str)

    def test_us_states_structure(self):
        """Test that US_STATES is a set of strings."""
        assert isinstance(EntityConfig.US_STATES, set)
        for state in EntityConfig.US_STATES:
            assert isinstance(state, str)
            assert len(state) == 2

    def test_street_suffixes_structure(self):
        """Test that street suffix lists are lists of strings."""
        assert isinstance(EntityConfig.STREET_SUFFIXES, list)
        for suffix in EntityConfig.STREET_SUFFIXES:
            assert isinstance(suffix, str)
        assert isinstance(EntityConfig.STREET_SUFFIXES_LOWER, list)
        for suffix in EntityConfig.STREET_SUFFIXES_LOWER:
            assert isinstance(suffix, str)

    def test_note_min_lengths(self):
        """Test the values and types of note minimum length configurations."""
        assert isinstance(EntityConfig.NOTE_MIN_ALPHANUMERIC, int)
        assert EntityConfig.NOTE_MIN_ALPHANUMERIC >= 0
        assert isinstance(EntityConfig.NOTE_MIN_LENGTH_OR_WORDS, int)
        assert EntityConfig.NOTE_MIN_LENGTH_OR_WORDS >= 0

    def test_name_excluded_words_structure(self):
        """Test that NAME_EXCLUDED_WORDS is a set of strings."""
        assert isinstance(EntityConfig.NAME_EXCLUDED_WORDS, set)
        for word in EntityConfig.NAME_EXCLUDED_WORDS:
            assert isinstance(word, str)

    def test_heuristic_stop_words_structure(self):
        """Test that HEURISTIC_STOP_WORDS is a set of strings."""
        assert isinstance(EntityConfig.HEURISTIC_STOP_WORDS, set)
        for word in EntityConfig.HEURISTIC_STOP_WORDS:
            assert isinstance(word, str)
