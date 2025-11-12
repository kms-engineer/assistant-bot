import pytest
from src.config.command_args_config import CommandArgsConfig


class TestCommandArgsConfig:
    """Tests for the CommandArgsConfig class."""

    def test_get_fields(self):
        """Test the _get_fields static method."""
        entities = {"name": "John", "phone": "123", "email": "a@b.com"}
        assert CommandArgsConfig._get_fields(entities, "name", "phone") == [
            "John",
            "123",
        ]
        assert CommandArgsConfig._get_fields(entities, "name", "address") == ["John"]
        assert CommandArgsConfig._get_fields(entities) == []

    def test_get_first(self):
        """Test the _get_first static method."""
        entities = {"name": "John", "phone": "123", "email": "a@b.com"}
        assert CommandArgsConfig._get_first(entities, "name", "phone") == ["John"]
        assert CommandArgsConfig._get_first(entities, "address", "email") == ["a@b.com"]
        assert CommandArgsConfig._get_first(entities, "address", "city") == []

    def test_with_default(self):
        """Test the _with_default static method."""
        entities = {"days": "10", "format": "list"}
        assert CommandArgsConfig._with_default(entities, "days", "7") == ["10"]
        assert CommandArgsConfig._with_default(entities, "sort", "date") == ["date"]

    def test_intent_arg_builders(self):
        """Test the INTENT_ARG_BUILDERS dictionary."""
        assert isinstance(CommandArgsConfig.INTENT_ARG_BUILDERS, dict)
        for intent, builder in CommandArgsConfig.INTENT_ARG_BUILDERS.items():
            assert callable(builder)

    def test_skip_pipeline_intents(self):
        """Test the SKIP_PIPELINE_INTENTS list."""
        assert isinstance(CommandArgsConfig.SKIP_PIPELINE_INTENTS, list)
        for intent in CommandArgsConfig.SKIP_PIPELINE_INTENTS:
            assert isinstance(intent, str)
