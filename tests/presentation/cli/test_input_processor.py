import pytest
from unittest.mock import MagicMock, patch

from src.presentation.cli.input_processor import process_classic_input


class TestProcessClassicInput:

    def test_process_valid_command(self):
        mock_parser = MagicMock()
        mock_parser.parse.return_value = ("add", ["Alice", "123"])

        mock_handler = MagicMock()
        mock_handler.handle.return_value = "Contact added"

        result = process_classic_input("add Alice 123", mock_parser, mock_handler)

        assert result == "Contact added"
        mock_handler.handle.assert_called_once_with("add", ["Alice", "123"])

    def test_process_with_cli_session_valid(self):
        mock_parser = MagicMock()
        mock_parser.parse.return_value = ("add", ["Alice"])

        mock_handler = MagicMock()
        mock_handler.handle.return_value = "Contact added"

        mock_session = MagicMock()
        mock_session.validate_command.return_value = None

        result = process_classic_input(
            "add Alice", mock_parser, mock_handler, mock_session
        )

        assert result == "Contact added"
        mock_session.validate_command.assert_called_once_with("add")

    def test_process_with_cli_session_invalid_command(self):
        mock_parser = MagicMock()
        mock_parser.parse.return_value = ("xyz", [])

        mock_handler = MagicMock()

        mock_session = MagicMock()
        mock_session.validate_command.return_value = "search"

        result = process_classic_input(
            "xyz", mock_parser, mock_handler, mock_session
        )

        assert result == ""
        mock_session.show_suggestion.assert_called_once_with("xyz", "search")
        mock_handler.handle.assert_not_called()

    def test_process_empty_command(self):
        mock_parser = MagicMock()
        mock_parser.parse.return_value = ("", [])

        mock_handler = MagicMock()
        mock_handler.handle.return_value = ""

        result = process_classic_input("", mock_parser, mock_handler)

        mock_handler.handle.assert_called_once_with("", [])

    def test_process_without_cli_session(self):
        mock_parser = MagicMock()
        mock_parser.parse.return_value = ("invalid", [])

        mock_handler = MagicMock()
        mock_handler.handle.return_value = "Invalid command message"

        result = process_classic_input("invalid", mock_parser, mock_handler)

        assert result == "Invalid command message"
        mock_handler.handle.assert_called_once()
