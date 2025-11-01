import pytest
from src.config.ui_config import UIConfig


class TestUIConfig:
    """Tests for the UIConfig class."""

    def test_classic_command_suggestion_cutoff_value(self):
        """Test the value and type of CLASSIC_COMMAND_SUGGESTION_CUTOFF."""
        assert isinstance(UIConfig.CLASSIC_COMMAND_SUGGESTION_CUTOFF, float)
        assert 0.0 <= UIConfig.CLASSIC_COMMAND_SUGGESTION_CUTOFF <= 1.0
