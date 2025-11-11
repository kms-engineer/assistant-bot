import pytest
from src.config.confidence_config import ConfidenceConfig


class TestConfidenceConfig:
    """Tests for the ConfidenceConfig class."""

    def test_all_confidence_scores_are_floats_in_range(self):
        """Test that all confidence scores are floats between 0.0 and 1.0."""
        for attr_name in dir(ConfidenceConfig):
            if attr_name.endswith("_CONFIDENCE"):
                confidence_value = getattr(ConfidenceConfig, attr_name)
                assert isinstance(
                    confidence_value, float
                ), f"{attr_name} is not a float"
                assert (
                    0.0 <= confidence_value <= 1.0
                ), f"{attr_name} is not in range [0.0, 1.0]"
