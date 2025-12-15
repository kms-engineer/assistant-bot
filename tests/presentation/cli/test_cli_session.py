import pytest
from unittest.mock import MagicMock, patch

from src.presentation.cli.cli_session import CLISession, create_cli_session


class TestCLISession:

    def test_init_with_commands(self):
        session = CLISession(commands=["add", "delete", "search"], use_prompt_toolkit=False)

        assert "add" in session._commands
        assert "delete" in session._commands

    def test_validate_command_valid(self):
        session = CLISession(commands=["add", "delete"], use_prompt_toolkit=False)
        result = session.validate_command("add")

        assert result is None

    def test_validate_command_exit(self):
        session = CLISession(commands=["add"], use_prompt_toolkit=False)
        result = session.validate_command("exit")

        assert result is None

    def test_validate_command_close(self):
        session = CLISession(commands=["add"], use_prompt_toolkit=False)
        result = session.validate_command("close")

        assert result is None

    def test_validate_command_invalid_with_suggestion(self):
        session = CLISession(commands=["add", "delete", "search"], use_prompt_toolkit=False)
        result = session.validate_command("ad")

        assert result == "add"

    def test_validate_command_invalid_no_suggestion(self):
        session = CLISession(commands=["add", "delete"], use_prompt_toolkit=False)
        result = session.validate_command("xyz")

        assert result is None

    def test_get_matching_commands_empty_prefix(self):
        session = CLISession(commands=["add", "delete", "search"], use_prompt_toolkit=False)
        matches = session.get_matching_commands("")

        assert len(matches) == 3

    def test_get_matching_commands_with_prefix(self):
        session = CLISession(commands=["add", "add-note", "delete"], use_prompt_toolkit=False)
        matches = session.get_matching_commands("add")

        assert "add" in matches
        assert "add-note" in matches
        assert "delete" not in matches

    def test_get_matching_commands_case_insensitive(self):
        session = CLISession(commands=["Add", "Delete"], use_prompt_toolkit=False)
        matches = session.get_matching_commands("a")

        assert "Add" in matches

    def test_update_commands(self):
        session = CLISession(commands=["old"], use_prompt_toolkit=False)
        session.update_commands(["new", "commands"])

        assert "old" not in session._commands
        assert "new" in session._commands
        assert "commands" in session._commands

    @patch("builtins.input", return_value="test input")
    def test_input_returns_stripped(self, mock_input):
        session = CLISession(commands=["add"], use_prompt_toolkit=False)
        result = session.input("prompt: ")

        assert result == "test input"

    @patch("builtins.input", return_value="  spaced  ")
    def test_input_strips_whitespace(self, mock_input):
        session = CLISession(commands=["add"], use_prompt_toolkit=False)
        result = session.input("prompt: ")

        assert result == "spaced"

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    def test_input_keyboard_interrupt(self, mock_input):
        session = CLISession(commands=["add"], use_prompt_toolkit=False)

        with pytest.raises(KeyboardInterrupt):
            session.input("prompt: ")

    @patch("builtins.input", side_effect=EOFError)
    def test_input_eof_error(self, mock_input):
        session = CLISession(commands=["add"], use_prompt_toolkit=False)

        with pytest.raises(EOFError):
            session.input("prompt: ")

    @patch("builtins.print")
    def test_show_suggestion_with_match(self, mock_print):
        session = CLISession(commands=["add"], use_prompt_toolkit=False)
        session.show_suggestion("ad", "add")

        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        assert "ad" in call_args
        assert "add" in call_args

    @patch("builtins.print")
    def test_show_suggestion_no_match(self, mock_print):
        session = CLISession(commands=["add"], use_prompt_toolkit=False)
        session.show_suggestion("xyz", None)

        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        assert "xyz" in call_args
        assert "help" in call_args

    def test_show_instant_suggestions(self):
        """Test that show_instant_suggestions does nothing (placeholder for prompt_toolkit)."""
        session = CLISession(commands=["add", "add-note", "delete"], use_prompt_toolkit=False)
        # Method should do nothing - autocomplete is handled by prompt_toolkit
        session.show_instant_suggestions("add")

    def test_show_instant_suggestions_empty(self):
        """Test that show_instant_suggestions does nothing with empty input."""
        session = CLISession(commands=["add"], use_prompt_toolkit=False)
        # Method should do nothing
        session.show_instant_suggestions("")

    def test_select_command_single_match(self):
        session = CLISession(commands=["add"], use_prompt_toolkit=False)
        result = session.select_command(["add"])

        assert result == "add"

    def test_select_command_empty(self):
        session = CLISession(commands=["add"], use_prompt_toolkit=False)
        result = session.select_command([])

        assert result is None


class TestCLISessionWithServices:

    def test_contact_name_provider(self):
        mock_service = MagicMock()
        mock_contact = MagicMock()
        mock_contact.name.value = "Alice"
        mock_service.get_all_contacts.return_value = [mock_contact]

        session = CLISession(
            commands=["add"],
            contact_service=mock_service,
            use_prompt_toolkit=False,
        )

        names = session._get_contact_names()
        assert "Alice" in names

    def test_contact_name_provider_error(self):
        mock_service = MagicMock()
        mock_service.get_all_contacts.side_effect = Exception("DB error")

        session = CLISession(
            commands=["add"],
            contact_service=mock_service,
            use_prompt_toolkit=False,
        )

        names = session._get_contact_names()
        assert names == []

    def test_search_suggestions_provider(self):
        mock_service = MagicMock()
        mock_contact = MagicMock()
        mock_contact.name.value = "Alice"
        mock_contact.email.value = "alice@test.com"
        mock_contact.phones = []
        mock_service.get_all_contacts.return_value = [mock_contact]

        session = CLISession(
            commands=["search"],
            contact_service=mock_service,
            use_prompt_toolkit=False,
        )

        suggestions = session._get_search_suggestions()
        assert "Alice" in suggestions
        assert "alice@test.com" in suggestions

    def test_note_ids_provider(self):
        mock_service = MagicMock()
        mock_note = MagicMock()
        mock_note.id = "note-123"
        mock_service.get_all_notes.return_value = [mock_note]

        session = CLISession(
            commands=["show-note"],
            note_service=mock_service,
            use_prompt_toolkit=False,
        )

        ids = session._get_note_ids()
        assert "note-123" in ids

    def test_tags_provider(self):
        mock_service = MagicMock()
        mock_service.list_tags.return_value = {"work": 3, "personal": 2}

        session = CLISession(
            commands=["search-notes-by-tag"],
            note_service=mock_service,
            use_prompt_toolkit=False,
        )

        tags = session._get_tags()
        assert "work" in tags
        assert "personal" in tags


class TestCreateCLISession:

    def test_create_session_from_handler(self):
        mock_handler = MagicMock()
        mock_handler.get_available_commands.return_value = ["add", "delete"]

        session = create_cli_session(mock_handler, use_prompt_toolkit=False)

        assert "add" in session._commands
        assert "delete" in session._commands

    def test_create_session_with_services(self):
        mock_handler = MagicMock()
        mock_handler.get_available_commands.return_value = ["add"]
        mock_contact_service = MagicMock()
        mock_note_service = MagicMock()

        session = create_cli_session(
            mock_handler,
            contact_service=mock_contact_service,
            note_service=mock_note_service,
            use_prompt_toolkit=False,
        )

        assert session._contact_service == mock_contact_service
        assert session._note_service == mock_note_service
