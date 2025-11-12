import pytest
from unittest.mock import patch
from src.presentation.cli.confirmation import confirm_action


class TestConfirmAction:
    """Tests for the confirmation prompt functionality."""

    @patch("builtins.input", return_value="y")
    def test_confirm_action_yes(self, mock_input):
        """Test that 'y' returns True."""
        result = confirm_action("Delete contact?")
        assert result is True
        mock_input.assert_called_once()

    @patch("builtins.input", return_value="yes")
    def test_confirm_action_yes_full(self, mock_input):
        """Test that 'yes' returns True."""
        result = confirm_action("Delete contact?")
        assert result is True

    @patch("builtins.input", return_value="n")
    def test_confirm_action_no(self, mock_input):
        """Test that 'n' returns False."""
        result = confirm_action("Delete contact?")
        assert result is False

    @patch("builtins.input", return_value="no")
    def test_confirm_action_no_full(self, mock_input):
        """Test that 'no' returns False."""
        result = confirm_action("Delete contact?")
        assert result is False

    @patch("builtins.input", return_value="")
    def test_confirm_action_empty_default_false(self, mock_input):
        """Test that empty input with default=False returns False."""
        result = confirm_action("Delete contact?", default=False)
        assert result is False

    @patch("builtins.input", return_value="")
    def test_confirm_action_empty_default_true(self, mock_input):
        """Test that empty input with default=True returns True."""
        result = confirm_action("Load file?", default=True)
        assert result is True

    @patch("builtins.input", side_effect=["invalid", "maybe", "y"])
    @patch("builtins.print")
    def test_confirm_action_invalid_then_yes(self, mock_print, mock_input):
        """Test that invalid inputs loop until valid input."""
        result = confirm_action("Delete contact?")
        assert result is True
        assert mock_input.call_count == 3
        # Should print error message twice for invalid inputs
        assert mock_print.call_count == 2
        mock_print.assert_called_with("Please answer 'y' or 'n'.")

    @patch("builtins.input", side_effect=["x", "n"])
    @patch("builtins.print")
    def test_confirm_action_invalid_then_no(self, mock_print, mock_input):
        """Test that invalid input loops then accepts 'n'."""
        result = confirm_action("Delete contact?")
        assert result is False
        assert mock_input.call_count == 2
        mock_print.assert_called_once_with("Please answer 'y' or 'n'.")

    @patch("builtins.input", return_value="Y")
    def test_confirm_action_case_insensitive_yes(self, mock_input):
        """Test that 'Y' (uppercase) returns True."""
        result = confirm_action("Delete contact?")
        assert result is True

    @patch("builtins.input", return_value="N")
    def test_confirm_action_case_insensitive_no(self, mock_input):
        """Test that 'N' (uppercase) returns False."""
        result = confirm_action("Delete contact?")
        assert result is False

    @patch("builtins.input", return_value="  y  ")
    def test_confirm_action_whitespace_yes(self, mock_input):
        """Test that '  y  ' (with whitespace) returns True."""
        result = confirm_action("Delete contact?")
        assert result is True

    @patch("builtins.input", return_value="  n  ")
    def test_confirm_action_whitespace_no(self, mock_input):
        """Test that '  n  ' (with whitespace) returns False."""
        result = confirm_action("Delete contact?")
        assert result is False

    @patch("builtins.input", side_effect=EOFError)
    def test_confirm_action_eof_error(self, mock_input):
        """Test that EOFError returns False (safe default)."""
        result = confirm_action("Delete contact?")
        assert result is False

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    def test_confirm_action_keyboard_interrupt(self, mock_input):
        """Test that KeyboardInterrupt returns False (safe default)."""
        result = confirm_action("Delete contact?")
        assert result is False
