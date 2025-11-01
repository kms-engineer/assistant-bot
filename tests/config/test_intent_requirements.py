import pytest
from src.config.intent_requirements import INTENT_REQUIREMENTS


class TestIntentRequirements:
    """Tests for the INTENT_REQUIREMENTS configuration."""

    def test_intent_requirements_structure(self):
        """Test that INTENT_REQUIREMENTS has the correct structure."""
        assert isinstance(INTENT_REQUIREMENTS, dict)
        for intent, requirements in INTENT_REQUIREMENTS.items():
            assert isinstance(intent, str)
            assert isinstance(requirements, dict)
            assert "required" in requirements
            assert "optional" in requirements
            assert isinstance(requirements["required"], list)
            assert isinstance(requirements["optional"], list)
            for item in requirements["required"]:
                assert isinstance(item, str)
            for item in requirements["optional"]:
                assert isinstance(item, str)
