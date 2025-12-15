import pytest
from unittest.mock import patch, MagicMock

from src.presentation.cli.interactive_commands import (
    InteractiveAddContact,
    InteractiveAddNote,
    InteractiveChangePhone,
    InteractiveAddEmail,
    InteractiveAddBirthday,
    InteractiveAddAddress,
    interactive_add_contact,
    interactive_add_note,
    interactive_change_phone,
)


class TestInteractiveAddContact:

    @patch("builtins.input", side_effect=["John Doe", "1234567890", "", "", ""])
    def test_collect_required_fields_only(self, mock_input):
        collector = InteractiveAddContact()
        result = collector.collect()

        assert result.success is True
        assert result.values["name"] == "John Doe"
        assert result.values["phone"] == "1234567890"

    @patch("builtins.input", side_effect=[
        "John Doe",
        "1234567890",
        "john@example.com",
        "15.03.1990",
        "123 Main Street",
    ])
    def test_collect_all_fields(self, mock_input):
        collector = InteractiveAddContact()
        result = collector.collect()

        assert result.success is True
        assert result.values["name"] == "John Doe"
        assert result.values["phone"] == "1234567890"
        assert result.values["email"] == "john@example.com"
        assert result.values["birthday"] == "15.03.1990"
        assert result.values["address"] == "123 Main Street"

    @patch("builtins.input", side_effect=["John Doe", "1234567890", "", "", ""])
    def test_collect_skip_optional_fields(self, mock_input):
        collector = InteractiveAddContact()
        result = collector.collect()

        assert result.success is True
        assert result.values["name"] == "John Doe"
        assert result.values["phone"] == "1234567890"
        assert "email" not in result.values or result.values.get("email") == ""
        assert "birthday" not in result.values or result.values.get("birthday") == ""
        assert "address" not in result.values or result.values.get("address") == ""

    @patch("builtins.input", return_value="cancel")
    def test_collect_cancelled(self, mock_input):
        collector = InteractiveAddContact()
        result = collector.collect()

        assert result.success is False
        assert result.cancelled is True


class TestInteractiveAddNote:

    @patch("builtins.input", side_effect=["My Note Title", "Note content here", ""])
    def test_collect_without_tags(self, mock_input):
        collector = InteractiveAddNote()
        result = collector.collect()

        assert result.success is True
        assert result.values["title"] == "My Note Title"
        assert result.values["text"] == "Note content here"

    @patch("builtins.input", side_effect=[
        "Shopping List",
        "Milk, bread, eggs",
        "groceries, shopping, todo"
    ])
    def test_collect_with_tags(self, mock_input):
        collector = InteractiveAddNote()
        result = collector.collect()

        assert result.success is True
        assert result.values["title"] == "Shopping List"
        assert result.values["text"] == "Milk, bread, eggs"
        assert result.values["tags"] == ["groceries", "shopping", "todo"]

    @patch("builtins.input", return_value="cancel")
    def test_collect_cancelled(self, mock_input):
        collector = InteractiveAddNote()
        result = collector.collect()

        assert result.success is False
        assert result.cancelled is True


class TestInteractiveChangePhone:

    @patch("builtins.input", side_effect=["John Doe", "1234567890", "0987654321"])
    def test_collect_all_fields(self, mock_input):
        collector = InteractiveChangePhone()
        result = collector.collect()

        assert result.success is True
        assert result.values["name"] == "John Doe"
        assert result.values["old_phone"] == "1234567890"
        assert result.values["new_phone"] == "0987654321"

    @patch("builtins.input", side_effect=["Jo", "1234567890", "0987654321"])
    def test_with_contact_names_autocomplete(self, mock_input):
        contact_names = ["John Doe", "Jane Smith"]
        collector = InteractiveChangePhone(contact_names)
        result = collector.collect()

        assert result.success is True

    @patch("builtins.input", return_value="cancel")
    def test_collect_cancelled(self, mock_input):
        collector = InteractiveChangePhone()
        result = collector.collect()

        assert result.success is False
        assert result.cancelled is True


class TestInteractiveAddEmail:

    @patch("builtins.input", side_effect=["John Doe", "john@example.com"])
    def test_collect_fields(self, mock_input):
        collector = InteractiveAddEmail()
        result = collector.collect()

        assert result.success is True
        assert result.values["name"] == "John Doe"
        assert result.values["email"] == "john@example.com"

    @patch("builtins.input", return_value="cancel")
    def test_collect_cancelled(self, mock_input):
        collector = InteractiveAddEmail()
        result = collector.collect()

        assert result.success is False


class TestInteractiveAddBirthday:

    @patch("builtins.input", side_effect=["John Doe", "15.03.1990"])
    def test_collect_fields(self, mock_input):
        collector = InteractiveAddBirthday()
        result = collector.collect()

        assert result.success is True
        assert result.values["name"] == "John Doe"
        assert result.values["birthday"] == "15.03.1990"

    @patch("builtins.input", return_value="cancel")
    def test_collect_cancelled(self, mock_input):
        collector = InteractiveAddBirthday()
        result = collector.collect()

        assert result.success is False


class TestInteractiveAddAddress:

    @patch("builtins.input", side_effect=["John Doe", "123 Main Street"])
    def test_collect_fields(self, mock_input):
        collector = InteractiveAddAddress()
        result = collector.collect()

        assert result.success is True
        assert result.values["name"] == "John Doe"
        assert result.values["address"] == "123 Main Street"

    @patch("builtins.input", return_value="cancel")
    def test_collect_cancelled(self, mock_input):
        collector = InteractiveAddAddress()
        result = collector.collect()

        assert result.success is False


class TestInteractiveAddContactFunction:

    @patch("builtins.input", side_effect=["John Doe", "1234567890", "", "", ""])
    def test_returns_args_and_optional_fields(self, mock_input):
        result = interactive_add_contact()

        assert result is not None
        args, optional = result
        assert args == ["John Doe", "1234567890"]
        assert isinstance(optional, dict)

    @patch("builtins.input", side_effect=[
        "John Doe",
        "1234567890",
        "john@example.com",
        "15.03.1990",
        "123 Main St",
    ])
    def test_returns_optional_fields_when_provided(self, mock_input):
        result = interactive_add_contact()

        assert result is not None
        args, optional = result
        assert args == ["John Doe", "1234567890"]
        assert optional.get("email") == "john@example.com"
        assert optional.get("birthday") == "15.03.1990"
        assert optional.get("address") == "123 Main St"

    @patch("builtins.input", return_value="cancel")
    def test_returns_none_when_cancelled(self, mock_input):
        result = interactive_add_contact()

        assert result is None


class TestInteractiveAddNoteFunction:

    @patch("builtins.input", side_effect=["My Title", "My content", ""])
    def test_returns_args_and_empty_tags(self, mock_input):
        result = interactive_add_note()

        assert result is not None
        args, tags = result
        assert args == ["My Title", "My content"]
        assert tags == []

    @patch("builtins.input", side_effect=["My Title", "My content", "tag1, tag2"])
    def test_returns_args_and_tags(self, mock_input):
        result = interactive_add_note()

        assert result is not None
        args, tags = result
        assert args == ["My Title", "My content"]
        assert tags == ["tag1", "tag2"]

    @patch("builtins.input", return_value="cancel")
    def test_returns_none_when_cancelled(self, mock_input):
        result = interactive_add_note()

        assert result is None


class TestInteractiveChangePhoneFunction:

    @patch("builtins.input", side_effect=["John Doe", "1234567890", "0987654321"])
    def test_returns_list_of_args(self, mock_input):
        result = interactive_change_phone()

        assert result is not None
        assert result == ["John Doe", "1234567890", "0987654321"]

    @patch("builtins.input", side_effect=["John Doe", "1234567890", "0987654321"])
    def test_with_contact_names(self, mock_input):
        result = interactive_change_phone(contact_names=["John Doe", "Jane Smith"])

        assert result is not None
        assert result[0] == "John Doe"

    @patch("builtins.input", return_value="cancel")
    def test_returns_none_when_cancelled(self, mock_input):
        result = interactive_change_phone()

        assert result is None
