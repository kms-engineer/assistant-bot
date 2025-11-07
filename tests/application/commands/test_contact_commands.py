import pytest
import os
from unittest.mock import Mock, patch
from src.application.commands import contact_commands
from src.domain.value_objects.name import Name
from src.domain.value_objects.phone import Phone
from src.domain.value_objects.email import Email
from src.domain.value_objects.address import Address
from src.domain.value_objects.birthday import Birthday
from src.domain.entities.contact import Contact
from src.presentation.cli.ui_messages import UIMessages


@pytest.fixture
def mock_service():
    """Create a mock ContactService for testing."""
    return Mock()


@pytest.fixture
def sample_contact():
    """Create a sample contact for testing."""
    contact = Contact(Name("John Doe"), "123")
    contact.add_phone(Phone("1234567890"))
    contact.add_email(Email("john.doe@example.com"))
    contact.add_address(Address("123 Main St"))
    contact.add_birthday(Birthday("01.01.1990"))
    return contact


class TestAddContact:
    """Tests for add_contact command."""

    def test_add_contact_success(self, mock_service):
        """Test adding a contact successfully."""
        mock_service.add_contact.return_value = "Contact added."
        result = contact_commands.add_contact(["John Doe", "1234567890"], mock_service)
        mock_service.add_contact.assert_called_once_with(Name("John Doe"), Phone("1234567890"))
        assert result == "Contact added."

    def test_add_contact_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(ValueError, match="Add command requires 2 arguments: name and phone"):
            contact_commands.add_contact(["John Doe"], mock_service)
        with pytest.raises(ValueError, match="Add command requires 2 arguments: name and phone"):
            contact_commands.add_contact([], mock_service)


class TestChangeContact:
    """Tests for change_contact command."""

    def test_change_contact_success(self, mock_service):
        """Test changing a contact's phone number successfully."""
        mock_service.change_phone.return_value = "Phone number updated."
        result = contact_commands.change_contact(["John Doe", "1234567890", "0987654321"], mock_service)
        mock_service.change_phone.assert_called_once_with("John Doe", Phone("1234567890"), Phone("0987654321"))
        assert result == "Phone number updated."

    def test_change_contact_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(ValueError, match="Change command requires 3 arguments: name, old phone, and new phone"):
            contact_commands.change_contact(["John Doe", "1234567890"], mock_service)
        with pytest.raises(ValueError, match="Change command requires 3 arguments: name, old phone, and new phone"):
            contact_commands.change_contact(["John Doe"], mock_service)
        with pytest.raises(ValueError, match="Change command requires 3 arguments: name, old phone, and new phone"):
            contact_commands.change_contact([], mock_service)


class TestDeleteContact:
    """Tests for delete_contact command."""

    @patch('src.application.commands.contact_commands.confirm_action')
    def test_delete_contact_success(self, mock_confirm_action, mock_service):
        """Test deleting a contact successfully with confirmation."""
        mock_confirm_action.return_value = True
        mock_service.delete_contact.return_value = "Contact deleted."
        result = contact_commands.delete_contact(["John Doe"], mock_service)
        mock_confirm_action.assert_called_once_with(UIMessages.CONFIRM_DELETE_CONTACT.format(name="John Doe"), default=False)
        mock_service.delete_contact.assert_called_once_with("John Doe")
        assert result == "Contact deleted."

    @patch('src.application.commands.contact_commands.confirm_action')
    def test_delete_contact_cancelled(self, mock_confirm_action, mock_service):
        """Test deleting a contact when action is cancelled."""
        mock_confirm_action.return_value = False
        result = contact_commands.delete_contact(["John Doe"], mock_service)
        mock_confirm_action.assert_called_once_with(UIMessages.CONFIRM_DELETE_CONTACT.format(name="John Doe"), default=False)
        mock_service.delete_contact.assert_not_called()
        assert result == UIMessages.ACTION_CANCELLED

    def test_delete_contact_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(ValueError, match="Delete-contact command requires 1 argument: name"):
            contact_commands.delete_contact([], mock_service)


class TestShowPhone:
    """Tests for show_phone command."""

    def test_show_phone_success(self, mock_service):
        """Test showing a contact's phone numbers."""
        mock_service.get_phones.return_value = ["1234567890", "0987654321"]
        result = contact_commands.show_phone(["John Doe"], mock_service)
        mock_service.get_phones.assert_called_once_with("John Doe")
        assert result == "John Doe: 1234567890; 0987654321"

    def test_show_phone_no_phones(self, mock_service):
        """Test showing phone numbers when none exist."""
        mock_service.get_phones.return_value = []
        result = contact_commands.show_phone(["John Doe"], mock_service)
        assert result == "John Doe has no phone numbers."

    def test_show_phone_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(ValueError, match="Phone command requires 1 argument: name"):
            contact_commands.show_phone([], mock_service)


class TestShowAll:
    """Tests for show_all command."""

    def test_show_all_with_contacts(self, mock_service, sample_contact):
        """Test showing all contacts when contacts exist."""
        mock_service.get_all_contacts.return_value = [sample_contact]
        result = contact_commands.show_all(mock_service)
        mock_service.get_all_contacts.assert_called_once()
        assert "All contacts:" in result
        assert str(sample_contact) in result

    def test_show_all_no_contacts(self, mock_service):
        """Test showing all contacts when no contacts exist."""
        mock_service.get_all_contacts.return_value = []
        result = contact_commands.show_all(mock_service)
        assert result == "No contacts found."


class TestAddBirthday:
    """Tests for add_birthday command."""

    def test_add_birthday_success(self, mock_service):
        """Test adding a birthday successfully."""
        mock_service.add_birthday.return_value = "Birthday added."
        result = contact_commands.add_birthday(["John Doe", "01.01.1990"], mock_service)
        mock_service.add_birthday.assert_called_once_with("John Doe", Birthday("01.01.1990"))
        assert result == "Birthday added."

    def test_add_birthday_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(ValueError, match="Add-birthday command requires 2 arguments: name and birthday \(DD.MM.YYYY\)"):
            contact_commands.add_birthday(["John Doe"], mock_service)
        with pytest.raises(ValueError, match="Add-birthday command requires 2 arguments: name and birthday \(DD.MM.YYYY\)"):
            contact_commands.add_birthday([], mock_service)


class TestShowBirthday:
    """Tests for show_birthday command."""

    def test_show_birthday_success(self, mock_service):
        """Test showing a contact's birthday."""
        mock_service.get_birthday.return_value = "01.01.1990"
        result = contact_commands.show_birthday(["John Doe"], mock_service)
        mock_service.get_birthday.assert_called_once_with("John Doe")
        assert result == "John Doe's birthday: 01.01.1990"

    def test_show_birthday_no_birthday(self, mock_service):
        """Test showing birthday when none is set."""
        mock_service.get_birthday.return_value = None
        result = contact_commands.show_birthday(["John Doe"], mock_service)
        assert result == "No birthday set for John Doe."

    def test_show_birthday_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(ValueError, match="Show-birthday command requires 1 argument: name"):
            contact_commands.show_birthday([], mock_service)


class TestBirthdays:
    """Tests for birthdays command."""

    def test_birthdays_default_days(self, mock_service):
        """Test showing upcoming birthdays with default days."""
        mock_service.get_upcoming_birthdays.return_value = [{"name": "John Doe", "birthdays_date": "01.01.2025"}]
        result = contact_commands.birthdays([], mock_service)
        mock_service.get_upcoming_birthdays.assert_called_once_with(7)
        assert "Upcoming birthdays:" in result
        assert "John Doe: 01.01.2025" in result

    def test_birthdays_specified_days(self, mock_service):
        """Test showing upcoming birthdays with specified days."""
        mock_service.get_upcoming_birthdays.return_value = [{"name": "Jane Doe", "birthdays_date": "05.02.2025"}]
        result = contact_commands.birthdays(["30"], mock_service)
        mock_service.get_upcoming_birthdays.assert_called_once_with(30)
        assert "Upcoming birthdays:" in result
        assert "Jane Doe: 05.02.2025" in result

    def test_birthdays_no_upcoming(self, mock_service):
        """Test showing upcoming birthdays when none are found."""
        mock_service.get_upcoming_birthdays.return_value = []
        result = contact_commands.birthdays(["10"], mock_service)
        assert result == "No upcoming birthdays in the next 10 days."

    def test_birthdays_invalid_days_type(self, mock_service):
        """Test that invalid days argument raises ValueError."""
        with pytest.raises(ValueError, match="Invalid amount of days ahead: abc"):
            contact_commands.birthdays(["abc"], mock_service)

    def test_birthdays_days_too_large(self, mock_service):
        """Test that days argument larger than 365 returns an error message."""
        result = contact_commands.birthdays(["366"], mock_service)
        assert result == "Max amount of days for upcoming birthdays is 365."


class TestAddEmail:
    """Tests for add_email command."""

    def test_add_email_success(self, mock_service):
        """Test adding an email successfully."""
        mock_service.add_email.return_value = "Email added."
        result = contact_commands.add_email(["John Doe", "john.doe@example.com"], mock_service)
        mock_service.add_email.assert_called_once_with("John Doe", Email("john.doe@example.com"))
        assert result == "Email added."

    def test_add_email_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(ValueError, match="Add-email command requires 2 arguments: name and email"):
            contact_commands.add_email(["John Doe"], mock_service)
        with pytest.raises(ValueError, match="Add-email command requires 2 arguments: name and email"):
            contact_commands.add_email([], mock_service)


class TestEditEmail:
    """Tests for edit_email command."""

    def test_edit_email_success(self, mock_service):
        """Test editing an email successfully."""
        mock_service.edit_email.return_value = "Email updated."
        result = contact_commands.edit_email(["John Doe", "new.email@example.com"], mock_service)
        mock_service.edit_email.assert_called_once_with("John Doe", Email("new.email@example.com"))
        assert result == "Email updated."

    def test_edit_email_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(ValueError, match="Edit-email command requires 2 arguments: name and new email address"):
            contact_commands.edit_email(["John Doe"], mock_service)
        with pytest.raises(ValueError, match="Edit-email command requires 2 arguments: name and new email address"):
            contact_commands.edit_email([], mock_service)


class TestRemoveEmail:
    """Tests for remove_email command."""

    @patch('src.application.commands.contact_commands.confirm_action')
    def test_remove_email_success(self, mock_confirm_action, mock_service):
        """Test removing an email successfully with confirmation."""
        mock_confirm_action.return_value = True
        mock_service.remove_email.return_value = "Email removed."
        result = contact_commands.remove_email(["John Doe"], mock_service)
        mock_confirm_action.assert_called_once_with(UIMessages.CONFIRM_REMOVE_EMAIL.format(name="John Doe"), default=False)
        mock_service.remove_email.assert_called_once_with("John Doe")
        assert result == "Email removed."

    @patch('src.application.commands.contact_commands.confirm_action')
    def test_remove_email_cancelled(self, mock_confirm_action, mock_service):
        """Test removing an email when action is cancelled."""
        mock_confirm_action.return_value = False
        result = contact_commands.remove_email(["John Doe"], mock_service)
        mock_confirm_action.assert_called_once_with(UIMessages.CONFIRM_REMOVE_EMAIL.format(name="John Doe"), default=False)
        mock_service.remove_email.assert_not_called()
        assert result == UIMessages.ACTION_CANCELLED

    def test_remove_email_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(ValueError, match="Remove-email command requires 1 argument: name"):
            contact_commands.remove_email([], mock_service)


class TestAddAddress:
    """Tests for add_address command."""

    def test_add_address_success(self, mock_service):
        """Test adding an address successfully."""
        mock_service.add_address.return_value = "Address added."
        result = contact_commands.add_address(["John Doe", "123", "Main", "St"], mock_service)
        mock_service.add_address.assert_called_once_with("John Doe", Address("123 Main St"))
        assert result == "Address added."

    def test_add_address_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(ValueError, match="Add-address command requires 2 arguments: name and address"):
            contact_commands.add_address(["John Doe"], mock_service)
        with pytest.raises(ValueError, match="Add-address command requires 2 arguments: name and address"):
            contact_commands.add_address([], mock_service)


class TestEditAddress:
    """Tests for edit_address command."""

    def test_edit_address_success(self, mock_service):
        """Test editing an address successfully."""
        mock_service.edit_address.return_value = "Address updated."
        result = contact_commands.edit_address(["John Doe", "456", "Oak", "Ave"], mock_service)
        mock_service.edit_address.assert_called_once_with("John Doe", Address("456 Oak Ave"))
        assert result == "Address updated."

    def test_edit_address_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(ValueError, match="Edit-address command requires 2 arguments: name and new address"):
            contact_commands.edit_address([""], mock_service)
        with pytest.raises(ValueError, match="Edit-address command requires 2 arguments: name and new address"):
            contact_commands.edit_address([], mock_service)


class TestRemoveAddress:
    """Tests for remove_address command."""

    @patch('src.application.commands.contact_commands.confirm_action')
    def test_remove_address_success(self, mock_confirm_action, mock_service):
        """Test removing an address successfully with confirmation."""
        mock_confirm_action.return_value = True
        mock_service.remove_address.return_value = "Address removed."
        result = contact_commands.remove_address(["John Doe"], mock_service)
        mock_confirm_action.assert_called_once_with(UIMessages.CONFIRM_REMOVE_ADDRESS.format(name="John Doe"), default=False)
        mock_service.remove_address.assert_called_once_with("John Doe")
        assert result == "Address removed."

    @patch('src.application.commands.contact_commands.confirm_action')
    def test_remove_address_cancelled(self, mock_confirm_action, mock_service):
        """Test removing an address when action is cancelled."""
        mock_confirm_action.return_value = False
        result = contact_commands.remove_address(["John Doe"], mock_service)
        mock_confirm_action.assert_called_once_with(UIMessages.CONFIRM_REMOVE_ADDRESS.format(name="John Doe"), default=False)
        mock_service.remove_address.assert_not_called()
        assert result == UIMessages.ACTION_CANCELLED

    def test_remove_address_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(ValueError, match="Remove-address command requires 1 argument: name"):
            contact_commands.remove_address([], mock_service)


class TestSearch:
    """Tests for search command."""

    def test_search_with_results(self, mock_service, sample_contact):
        """Test searching contacts with matching results."""
        mock_service.search.return_value = [sample_contact]
        result = contact_commands.search(["John"], mock_service)
        mock_service.search.assert_called_once_with("John")
        assert "Found contacts:" in result
        assert str(sample_contact) in result

    def test_search_no_results(self, mock_service):
        """Test searching contacts without matches."""
        mock_service.search.return_value = []
        result = contact_commands.search(["NonExistent"], mock_service)
        assert result == "No contact name, email or phone found for provided search text: NonExistent"

    def test_search_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(ValueError, match="Search command requires a search_text argument"):
            contact_commands.search([], mock_service)


class TestFind:
    """Tests for find command (exact search)."""

    def test_find_with_results(self, mock_service, sample_contact):
        """Test finding contacts with exact matching results."""
        mock_service.search.return_value = [sample_contact]
        result = contact_commands.find(["John Doe"], mock_service)
        mock_service.search.assert_called_once_with("John Doe", exact=True)
        assert "Found contacts:" in result
        assert str(sample_contact) in result

    def test_find_no_results(self, mock_service):
        """Test finding contacts without exact matches."""
        mock_service.search.return_value = []
        result = contact_commands.find(["NonExistent"], mock_service)
        assert result == "No contact name, email or phone found for provided search text: NonExistent"

    def test_find_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(ValueError, match="Find command requires a search_text argument"):
            contact_commands.find([], mock_service)


class TestSaveContacts:
    """Tests for save_contacts command."""

    def test_save_contacts_success(self, mock_service):
        """Test saving contacts successfully."""
        mock_service.save_address_book.return_value = "contacts.json"
        result = contact_commands.save_contacts(["contacts.json"], mock_service)
        mock_service.save_address_book.assert_called_once_with("contacts.json", user_provided=True)
        assert result == "Address book saved to contacts.json."

    def test_save_contacts_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(ValueError, match="Save command requires a filename argument"):
            contact_commands.save_contacts([], mock_service)


class TestLoadContacts:
    """Tests for load_contacts command."""

    @patch('src.application.commands.contact_commands.confirm_action')
    def test_load_contacts_success(self, mock_confirm_action, mock_service):
        """Test loading contacts successfully with confirmation."""
        mock_confirm_action.return_value = True
        mock_service.load_address_book.return_value = 5
        mock_service.get_current_filename.return_value = "loaded_contacts.json"
        result = contact_commands.load_contacts(["my_contacts.json"], mock_service)
        mock_confirm_action.assert_called_once_with(UIMessages.CONFIRM_LOAD_FILE, default=False)
        mock_service.load_address_book.assert_called_once_with("my_contacts.json", user_provided=True)
        mock_service.get_current_filename.assert_called_once()
        assert result == "Address book loaded from loaded_contacts.json. 5 contact(s) found."

    @patch('src.application.commands.contact_commands.confirm_action')
    def test_load_contacts_cancelled(self, mock_confirm_action, mock_service):
        """Test loading contacts when action is cancelled."""
        mock_confirm_action.return_value = False
        result = contact_commands.load_contacts(["my_contacts.json"], mock_service)
        mock_confirm_action.assert_called_once_with(UIMessages.CONFIRM_LOAD_FILE, default=False)
        mock_service.load_address_book.assert_not_called()
        assert result == UIMessages.ACTION_CANCELLED

    def test_load_contacts_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(ValueError, match="Load command requires a filename argument"):
            contact_commands.load_contacts([], mock_service)


class TestHello:
    """Tests for hello command."""

    def test_hello_command(self, mock_service):
        """Test the hello command returns the correct greeting."""
        result = contact_commands.hello()
        assert result == "How can I help you?"


class TestHelp:
    """Tests for help command."""

    def test_help_command_default(self, mock_service):
        """Test the help command returns the command list."""
        with patch.object(UIMessages, 'get_command_list', return_value="Command List") as mock_get_command_list:
            result = contact_commands.help()
            mock_get_command_list.assert_called_once_with(False)
            assert result == "Command List"

    def test_help_command_nlp_mode(self, mock_service):
        """Test the help command returns the command list in NLP mode."""
        with patch.object(UIMessages, 'get_command_list', return_value="NLP Command List") as mock_get_command_list:
            result = contact_commands.help(nlp_mode=True)
            mock_get_command_list.assert_called_once_with(True)
            assert result == "NLP Command List"


class TestClear:
    """Tests for clear command."""

    @patch('os.system')
    def test_clear_command(self, mock_os_system, mock_service):
        """Test the clear command calls os.system with correct argument."""
        result = contact_commands.clear()
        if os.name == 'posix':
            mock_os_system.assert_called_once_with('clear')
        else:
            mock_os_system.assert_called_once_with('cls')
        assert result == ""
