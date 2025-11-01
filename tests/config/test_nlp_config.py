import pytest
from src.config.nlp_config import NLPConfig


class TestNLPConfig:
    """Tests for the NLPConfig class."""

    def test_intent_confidence_threshold(self):
        """Test the value and type of INTENT_CONFIDENCE_THRESHOLD."""
        assert isinstance(NLPConfig.INTENT_CONFIDENCE_THRESHOLD, float)
        assert 0.0 <= NLPConfig.INTENT_CONFIDENCE_THRESHOLD <= 1.0

    def test_entity_confidence_threshold(self):
        """Test the value and type of ENTITY_CONFIDENCE_THRESHOLD."""
        assert isinstance(NLPConfig.ENTITY_CONFIDENCE_THRESHOLD, float)
        assert 0.0 <= NLPConfig.ENTITY_CONFIDENCE_THRESHOLD <= 1.0

    def test_confidence_override_threshold(self):
        """Test the value and type of CONFIDENCE_OVERRIDE_THRESHOLD."""
        assert isinstance(NLPConfig.CONFIDENCE_OVERRIDE_THRESHOLD, float)
        assert 0.0 <= NLPConfig.CONFIDENCE_OVERRIDE_THRESHOLD <= 1.0

    def test_low_confidence_threshold(self):
        """Test the value and type of LOW_CONFIDENCE_THRESHOLD."""
        assert isinstance(NLPConfig.LOW_CONFIDENCE_THRESHOLD, float)
        assert 0.0 <= NLPConfig.LOW_CONFIDENCE_THRESHOLD <= 1.0

    def test_command_suggestion_cutoff(self):
        """Test the value and type of COMMAND_SUGGESTION_CUTOFF."""
        assert isinstance(NLPConfig.COMMAND_SUGGESTION_CUTOFF, float)
        assert 0.0 <= NLPConfig.COMMAND_SUGGESTION_CUTOFF <= 1.0

    def test_default_region(self):
        """Test the value and type of DEFAULT_REGION."""
        assert isinstance(NLPConfig.DEFAULT_REGION, str)
        assert len(NLPConfig.DEFAULT_REGION) == 2
