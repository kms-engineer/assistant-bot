import pytest
from src.config.pipeline_definitions import PIPELINE_DEFINITIONS


class TestPipelineDefinitions:
    """Tests for the PIPELINE_DEFINITIONS configuration."""

    def test_pipeline_definitions_structure(self):
        """Test that PIPELINE_DEFINITIONS has the correct structure."""
        assert isinstance(PIPELINE_DEFINITIONS, dict)
        for intent, definition in PIPELINE_DEFINITIONS.items():
            assert isinstance(intent, str)
            assert isinstance(definition, dict)
            assert "primary_command" in definition
            assert isinstance(definition["primary_command"], str)
            assert "primary_required" in definition
            assert isinstance(definition["primary_required"], list)
            for item in definition["primary_required"]:
                assert isinstance(item, str)
            assert "pipeline" in definition
            assert isinstance(definition["pipeline"], list)
            for step in definition["pipeline"]:
                assert isinstance(step, dict)
                assert "command" in step
                assert isinstance(step["command"], str)
                assert "entities" in step
                assert isinstance(step["entities"], list)
                for entity in step["entities"]:
                    assert isinstance(entity, str)
                assert "min_entities" in step
                assert isinstance(step["min_entities"], int)
