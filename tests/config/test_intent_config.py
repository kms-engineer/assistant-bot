import pytest
from src.config.intent_config import IntentConfig


class TestIntentConfig:
    """Tests for the IntentConfig class."""

    def test_intent_labels_structure(self):
        """Test that INTENT_LABELS is a list of strings."""
        assert isinstance(IntentConfig.INTENT_LABELS, list)
        for label in IntentConfig.INTENT_LABELS:
            assert isinstance(label, str)

    def test_intent_to_command_map_structure(self):
        """Test that INTENT_TO_COMMAND_MAP is a dictionary of strings."""
        assert isinstance(IntentConfig.INTENT_TO_COMMAND_MAP, dict)
        for key, value in IntentConfig.INTENT_TO_COMMAND_MAP.items():
            assert isinstance(key, str)
            assert isinstance(value, str)

    def test_keyword_confidence_values(self):
        """Test the values and types of keyword confidence scores."""
        assert isinstance(IntentConfig.KEYWORD_CONFIDENCE_MIN, float)
        assert 0.0 <= IntentConfig.KEYWORD_CONFIDENCE_MIN <= 1.0
        assert isinstance(IntentConfig.KEYWORD_CONFIDENCE_MAX, float)
        assert 0.0 <= IntentConfig.KEYWORD_CONFIDENCE_MAX <= 1.0
        assert (
            IntentConfig.KEYWORD_CONFIDENCE_MIN <= IntentConfig.KEYWORD_CONFIDENCE_MAX
        )

    def test_default_intent_values(self):
        """Test the values and types of default intent configurations."""
        assert isinstance(IntentConfig.DEFAULT_INTENT, str)
        assert IntentConfig.DEFAULT_INTENT in IntentConfig.INTENT_LABELS
        assert isinstance(IntentConfig.DEFAULT_INTENT_CONFIDENCE, float)
        assert 0.0 <= IntentConfig.DEFAULT_INTENT_CONFIDENCE <= 1.0

    def test_imported_data_structures(self):
        """Test that the imported data structures are not empty."""
        assert isinstance(IntentConfig.KEYWORD_MAP, dict)
        assert len(IntentConfig.KEYWORD_MAP) > 0
        assert isinstance(IntentConfig.PIPELINE_DEFINITIONS, dict)
        assert len(IntentConfig.PIPELINE_DEFINITIONS) > 0
        assert isinstance(IntentConfig.INTENT_REQUIREMENTS, dict)
        assert len(IntentConfig.INTENT_REQUIREMENTS) > 0
