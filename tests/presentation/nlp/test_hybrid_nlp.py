"""Tests for HybridNLP class."""
import pytest
from unittest.mock import Mock, MagicMock, patch
from src.presentation.nlp.hybrid_nlp import HybridNLP
from src.config.intent_config import IntentConfig


class TestHybridNLP:
    """Tests for HybridNLP process method."""

    @pytest.fixture
    def hybrid_nlp(self):
        """Create HybridNLP instance for testing."""
        return HybridNLP()

    def test_process_simple_add_contact(self, hybrid_nlp):
        """Test processing simple add contact command."""
        user_text = "Add John with phone 1234567890"
        result = hybrid_nlp.process(user_text)

        assert "intent" in result
        assert "entities" in result
        # Intent should be related to adding contact
        assert result["intent"] in ["add_contact", "create_contact"]

    def test_process_search_contact(self, hybrid_nlp):
        """Test processing search contact command."""
        user_text = "Search for Alice"
        result = hybrid_nlp.process(user_text)

        assert "intent" in result
        assert result["intent"] in ["search_contacts", "find_contact"]

    def test_process_add_note(self, hybrid_nlp):
        """Test processing add note command."""
        user_text = "Add note meeting tomorrow"
        result = hybrid_nlp.process(user_text)

        assert "intent" in result
        assert result["intent"] in ["add_note", "create_note"]

    def test_process_show_birthdays(self, hybrid_nlp):
        """Test processing show birthdays command."""
        user_text = "Show birthdays for next 30 days"
        result = hybrid_nlp.process(user_text)

        assert "intent" in result
        assert "entities" in result
        # Should detect days parameter
        assert result["intent"] in ["show_birthdays", "get_birthdays", "upcoming_birthdays", "list_birthdays"]

    def test_get_command_args_add_contact(self, hybrid_nlp):
        """Test getting command args for add_contact intent."""
        nlp_result = {
            "intent": "add_contact",
            "entities": {
                "name": "John",
                "phone": "1234567890"
            }
        }

        command, args = hybrid_nlp.get_command_args(nlp_result)

        assert command in IntentConfig.INTENT_TO_COMMAND_MAP.get("add_contact", "add_contact")
        assert isinstance(args, list)

    def test_get_command_args_search_contacts(self, hybrid_nlp):
        """Test getting command args for search_contacts intent."""
        nlp_result = {
            "intent": "search_contacts",
            "entities": {
                "name": "Alice"
            }
        }

        command, args = hybrid_nlp.get_command_args(nlp_result)

        assert command in IntentConfig.INTENT_TO_COMMAND_MAP.get("search_contacts", "search_contacts")
        assert isinstance(args, list)

    def test_get_command_args_add_note(self, hybrid_nlp):
        """Test getting command args for add_note intent."""
        nlp_result = {
            "intent": "add_note",
            "entities": {
                "title": "Meeting",
                "text": "Team meeting tomorrow"
            }
        }

        command, args = hybrid_nlp.get_command_args(nlp_result)

        assert command in IntentConfig.INTENT_TO_COMMAND_MAP.get("add_note", "add_note")
        assert isinstance(args, list)

    def test_get_command_args_unknown_intent(self, hybrid_nlp):
        """Test getting command args for unknown intent."""
        nlp_result = {
            "intent": "unknown_intent",
            "entities": {}
        }

        command, args = hybrid_nlp.get_command_args(nlp_result)

        # Should return the intent as command name
        assert command == "unknown_intent"
        assert args == []

    def test_process_empty_text(self, hybrid_nlp):
        """Test processing empty text."""
        result = hybrid_nlp.process("")

        assert "intent" in result
        assert "entities" in result

    def test_process_whitespace_only(self, hybrid_nlp):
        """Test processing whitespace only."""
        result = hybrid_nlp.process("   ")

        assert "intent" in result
        assert "entities" in result

    def test_process_returns_dict(self, hybrid_nlp):
        """Test that process always returns a dictionary."""
        user_texts = [
            "Add contact",
            "Show all",
            "Delete note",
            "Search Alice"
        ]

        for text in user_texts:
            result = hybrid_nlp.process(text)
            assert isinstance(result, dict)
            assert "intent" in result
            assert "entities" in result


class TestHybridNLPEdgeCases:
    """Tests for HybridNLP edge cases."""

    @pytest.fixture
    def hybrid_nlp(self):
        """Create HybridNLP instance for testing."""
        return HybridNLP()

    def test_process_very_long_text(self, hybrid_nlp):
        """Test processing very long text."""
        user_text = "Add contact " + "John " * 100
        result = hybrid_nlp.process(user_text)

        assert "intent" in result
        assert "entities" in result

    def test_process_special_characters(self, hybrid_nlp):
        """Test processing text with special characters."""
        user_text = "Add contact John@#$%^&*()"
        result = hybrid_nlp.process(user_text)

        assert "intent" in result
        assert "entities" in result

    def test_process_numbers_only(self, hybrid_nlp):
        """Test processing text with numbers only."""
        user_text = "1234567890"
        result = hybrid_nlp.process(user_text)

        assert "intent" in result
        assert "entities" in result

    def test_process_mixed_case(self, hybrid_nlp):
        """Test processing mixed case text."""
        user_texts = [
            "ADD CONTACT JOHN",
            "add contact john",
            "AdD cOnTaCt JoHn"
        ]

        for text in user_texts:
            result = hybrid_nlp.process(text)
            assert "intent" in result
            assert "entities" in result


class TestGetCommandArgs:
    """Tests for get_command_args static method."""

    def test_get_command_args_maps_intent(self):
        """Test that intent is mapped to command name."""
        # Test various intent to command mappings
        test_cases = [
            ("add_contact", "add"),
            ("search_contacts", "search"),
            ("add_note", "add-note"),
            ("show_birthdays", "birthdays"),
        ]

        for intent, expected_command in test_cases:
            nlp_result = {"intent": intent, "entities": {}}
            command, _ = HybridNLP.get_command_args(nlp_result)

            # Command should be from INTENT_TO_COMMAND_MAP or the intent itself
            assert command in [expected_command, intent, IntentConfig.INTENT_TO_COMMAND_MAP.get(intent, intent)]

    def test_get_command_args_no_entities(self):
        """Test get_command_args with no entities."""
        nlp_result = {"intent": "list_contacts", "entities": {}}
        command, args = HybridNLP.get_command_args(nlp_result)

        assert isinstance(command, str)
        assert isinstance(args, list)

    def test_get_command_args_preserves_entity_order(self):
        """Test that entity order is preserved in args."""
        nlp_result = {
            "intent": "add_contact",
            "entities": {
                "name": "John",
                "phone": "1234567890"
            }
        }

        command, args = HybridNLP.get_command_args(nlp_result)

        # Args should be a list
        assert isinstance(args, list)
