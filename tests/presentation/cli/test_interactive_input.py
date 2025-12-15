import pytest
from unittest.mock import patch, MagicMock

from src.presentation.cli.interactive_input import (
    InputField,
    InputResult,
    InteractiveInputBuilder,
    QuickInput,
)


class TestInputField:

    def test_input_field_defaults(self):
        field = InputField(name="test", prompt="Enter value")

        assert field.name == "test"
        assert field.prompt == "Enter value"
        assert field.required is True
        assert field.validator is None
        assert field.default is None

    def test_input_field_optional(self):
        field = InputField(name="test", prompt="Enter value", required=False)

        assert field.required is False


class TestInputResult:

    def test_input_result_success(self):
        result = InputResult(success=True, values={"name": "Alice"})

        assert result.success is True
        assert result.values["name"] == "Alice"
        assert result.cancelled is False

    def test_input_result_cancelled(self):
        result = InputResult(success=False, cancelled=True)

        assert result.success is False
        assert result.cancelled is True

    def test_input_result_error(self):
        result = InputResult(success=False, error="Something went wrong")

        assert result.success is False
        assert result.error == "Something went wrong"


class TestInteractiveInputBuilder:

    @patch("builtins.input", return_value="Alice")
    def test_single_required_field(self, mock_input):
        builder = InteractiveInputBuilder()
        builder.add_field(name="name", prompt="Enter name")
        result = builder.build()

        assert result.success is True
        assert result.values["name"] == "Alice"

    @patch("builtins.input", side_effect=["Alice", "123-456"])
    def test_multiple_fields(self, mock_input):
        builder = InteractiveInputBuilder()
        builder.add_field(name="name", prompt="Enter name")
        builder.add_field(name="phone", prompt="Enter phone")
        result = builder.build()

        assert result.success is True
        assert result.values["name"] == "Alice"
        assert result.values["phone"] == "123-456"

    @patch("builtins.input", return_value="")
    def test_optional_field_skip(self, mock_input):
        builder = InteractiveInputBuilder()
        builder.add_field(name="email", prompt="Enter email", required=False)
        result = builder.build()

        assert result.success is True
        assert "email" not in result.values

    @patch("builtins.input", return_value="")
    def test_optional_field_with_default(self, mock_input):
        builder = InteractiveInputBuilder()
        builder.add_field(
            name="country",
            prompt="Enter country",
            required=False,
            default="USA",
        )
        result = builder.build()

        assert result.success is True
        assert result.values["country"] == "USA"

    @patch("builtins.input", side_effect=["", "Alice"])
    @patch("builtins.print")
    def test_required_field_empty_retry(self, mock_print, mock_input):
        builder = InteractiveInputBuilder()
        builder.add_field(name="name", prompt="Enter name")
        result = builder.build()

        assert result.success is True
        assert result.values["name"] == "Alice"
        assert mock_input.call_count == 2

    @patch("builtins.input", return_value="cancel")
    def test_cancel_command(self, mock_input):
        builder = InteractiveInputBuilder()
        builder.add_field(name="name", prompt="Enter name")
        result = builder.build()

        assert result.success is False
        assert result.cancelled is True

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    def test_keyboard_interrupt(self, mock_input):
        builder = InteractiveInputBuilder()
        builder.add_field(name="name", prompt="Enter name")
        result = builder.build()

        assert result.success is False
        assert result.cancelled is True

    @patch("builtins.input", side_effect=["invalid", "valid@email.com"])
    @patch("builtins.print")
    def test_validator_retry(self, mock_print, mock_input):
        def email_validator(value):
            return "@" in value

        builder = InteractiveInputBuilder()
        builder.add_field(
            name="email",
            prompt="Enter email",
            validator=email_validator,
            error_message="Invalid email format",
        )
        result = builder.build()

        assert result.success is True
        assert result.values["email"] == "valid@email.com"

    @patch("builtins.input", return_value="42")
    def test_transform_function(self, mock_input):
        builder = InteractiveInputBuilder()
        builder.add_field(
            name="age",
            prompt="Enter age",
            transform=int,
        )
        result = builder.build()

        assert result.success is True
        assert result.values["age"] == 42
        assert isinstance(result.values["age"], int)

    def test_reset_clears_fields(self):
        builder = InteractiveInputBuilder()
        builder.add_field(name="test", prompt="Test")
        builder.reset()

        assert len(builder._fields) == 0

    def test_fluent_interface(self):
        builder = (
            InteractiveInputBuilder()
            .add_field(name="a", prompt="A")
            .add_field(name="b", prompt="B")
            .show_progress(False)
            .allow_cancel(False)
        )

        assert len(builder._fields) == 2
        assert builder._show_progress is False
        assert builder._allow_cancel is False


class TestQuickInput:

    @patch("builtins.input", return_value="y")
    def test_confirm_yes(self, mock_input):
        result = QuickInput.confirm("Delete?")
        assert result is True

    @patch("builtins.input", return_value="n")
    def test_confirm_no(self, mock_input):
        result = QuickInput.confirm("Delete?")
        assert result is False

    @patch("builtins.input", return_value="")
    def test_confirm_default_false(self, mock_input):
        result = QuickInput.confirm("Delete?", default=False)
        assert result is False

    @patch("builtins.input", return_value="")
    def test_confirm_default_true(self, mock_input):
        result = QuickInput.confirm("Proceed?", default=True)
        assert result is True

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    def test_confirm_interrupt(self, mock_input):
        result = QuickInput.confirm("Delete?")
        assert result is False

    @patch("builtins.input", return_value="1")
    @patch("builtins.print")
    def test_select_first_option(self, mock_print, mock_input):
        result = QuickInput.select("Choose:", ["Option A", "Option B"])
        assert result == 0

    @patch("builtins.input", return_value="2")
    @patch("builtins.print")
    def test_select_second_option(self, mock_print, mock_input):
        result = QuickInput.select("Choose:", ["Option A", "Option B"])
        assert result == 1

    @patch("builtins.input", return_value="0")
    @patch("builtins.print")
    def test_select_cancel(self, mock_print, mock_input):
        result = QuickInput.select("Choose:", ["Option A"], allow_cancel=True)
        assert result is None

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    @patch("builtins.print")
    def test_select_interrupt(self, mock_print, mock_input):
        result = QuickInput.select("Choose:", ["Option A"])
        assert result is None

    @patch("builtins.input", return_value="test value")
    def test_text_valid(self, mock_input):
        result = QuickInput.text("Enter value")
        assert result == "test value"

    @patch("builtins.input", return_value="")
    def test_text_optional_empty(self, mock_input):
        result = QuickInput.text("Enter value", required=False)
        assert result is None

    @patch("builtins.input", side_effect=["", "value"])
    @patch("builtins.print")
    def test_text_required_retry(self, mock_print, mock_input):
        result = QuickInput.text("Enter value", required=True)
        assert result == "value"
        assert mock_input.call_count == 2

    @patch("builtins.input", side_effect=["bad", "good@email.com"])
    @patch("builtins.print")
    def test_text_with_validator(self, mock_print, mock_input):
        result = QuickInput.text(
            "Enter email",
            validator=lambda x: "@" in x,
            error_message="Invalid email",
        )
        assert result == "good@email.com"
