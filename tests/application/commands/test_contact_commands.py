import pytest
from unittest.mock import Mock, patch, MagicMock
from src.application.commands import contact_commands
from src.domain.value_objects.name import Name
from src.domain.value_objects.phone import Phone
from src.domain.value_objects.email import Email
from src.domain.value_objects.address import Address
from src.domain.value_objects.birthday import Birthday
from src.domain.entities.contact import Contact
from src.presentation.cli.ui_messages import UIMessages
from tests.application.commands import random_user, random_phone


@pytest.fixture
def mock_service():
    """Create a mock ContactService for testing."""
    return Mock()


@pytest.fixture
def sample_contact():
    """Create a sample contact for testing."""
    contact = Contact(Name("John Doe"), "contact-123")
    contact.add_phone(Phone("1234567890"))
    return contact


@pytest.fixture
def sample_contact_with_email():
    """Create a sample contact with email for testing."""
    contact = Contact(Name("John Doe"), "contact-123")
    contact.add_phone(Phone("1234567890"))
    contact.add_email(Email("john.doe@example.com"))
    return contact


@pytest.fixture
def sample_contact_with_birthday():
    """Create a sample contact with birthday for testing."""
    contact = Contact(Name("John Doe"), "contact-123")
    contact.add_phone(Phone("1234567890"))
    contact.add_birthday(Birthday("01.01.1990"))
    return contact


class TestAddContact:
    """Tests for add_contact command."""

    @patch("src.application.commands.contact_commands._select_contact_by_name")
    def test_add_contact_new(self, mock_select, mock_service):
        """Test adding a completely new contact."""
        # Mock _select_contact_by_name to return None (no existing contact)
        mock_service.find_all_by_name.return_value = []
        mock_select.return_value = None
        mock_service.add_contact.return_value = "New contact created"

        test_user = random_user()
        test_phone = random_phone()
        result = contact_commands.add_contact([test_user, test_phone], mock_service)

        mock_service.add_contact.assert_called_once_with(
            Name(test_user), Phone(test_phone)
        )
        assert result == "New contact created"

    @patch("src.application.commands.contact_commands._select_contact_by_name")
    @patch("builtins.input", return_value="1")
    def test_add_contact_existing(self, mock_select, mock_service, sample_contact):
        """Test adding phone to existing contact."""
        # Mock _select_contact_by_name to return existing contact
        mock_service.find_all_by_name.return_value = [sample_contact]
        mock_select.return_value = "1"
        mock_service.add_phone_to_contact.return_value = (
            "Phone added to existing contact"
        )

        result = contact_commands.add_contact(
            [sample_contact.name.value, sample_contact.phones[0].value], mock_service
        )

        mock_service.add_phone_to_contact.assert_called_once()
        assert "Phone added" in result or "existing contact" in result

    def test_add_contact_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(
            ValueError, match="Add command requires 2 arguments: name and phone"
        ):
            contact_commands.add_contact(["John Doe"], mock_service)
        with pytest.raises(
            ValueError, match="Add command requires 2 arguments: name and phone"
        ):
            contact_commands.add_contact([], mock_service)


class TestChangeContact:
    """Tests for change_contact command."""

    @patch("src.application.commands.contact_commands.confirm_action")
    @patch("src.application.commands.contact_commands._select_contact_by_name")
    def test_change_contact_success(
        self, mock_select, mock_confirm, mock_service, sample_contact
    ):
        """Test changing a contact's phone number successfully."""
        mock_select.return_value = sample_contact
        mock_confirm.return_value = True
        mock_service.edit_phone_by_id.return_value = "Phone number updated."

        result = contact_commands.change_contact(
            ["John Doe", "1234567890", "0987654321"], mock_service
        )

        mock_confirm.assert_called_once()
        mock_service.edit_phone_by_id.assert_called_once()
        assert result == "Phone number updated."

    @patch("src.application.commands.contact_commands.confirm_action")
    @patch("src.application.commands.contact_commands._select_contact_by_name")
    def test_change_contact_cancelled(
        self, mock_select, mock_confirm, mock_service, sample_contact
    ):
        """Test that cancelling change returns ACTION_CANCELLED."""
        mock_select.return_value = sample_contact
        mock_confirm.return_value = False

        result = contact_commands.change_contact(
            ["John Doe", "1234567890", "0987654321"], mock_service
        )

        assert result == UIMessages.ACTION_CANCELLED
        mock_service.edit_phone_by_id.assert_not_called()

    def test_change_contact_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(ValueError, match="Change command requires 3 arguments"):
            contact_commands.change_contact(["John Doe", "1234567890"], mock_service)


class TestDeleteContact:
    """Tests for delete_contact command."""

    @patch("src.application.commands.contact_commands.confirm_action")
    def test_delete_contact_success(self, mock_confirm, mock_service, sample_contact):
        """Test deleting a contact successfully with confirmation."""
        mock_confirm.return_value = True
        mock_service.find_all_by_name.return_value = [sample_contact]
        mock_service.delete_contact_by_id.return_value = "Contact deleted."

        result = contact_commands.delete_contact(["John Doe"], mock_service)

        mock_confirm.assert_called_once()
        mock_service.delete_contact_by_id.assert_called_once_with(sample_contact.id)
        assert result == "Contact deleted."

    @patch("src.application.commands.contact_commands.confirm_action")
    def test_delete_contact_cancelled(self, mock_confirm, mock_service, sample_contact):
        """Test deleting a contact when action is cancelled."""
        mock_confirm.return_value = False
        mock_service.find_all_by_name.return_value = [sample_contact]

        result = contact_commands.delete_contact(["John Doe"], mock_service)

        mock_confirm.assert_called_once()
        mock_service.delete_contact_by_id.assert_not_called()
        assert result == UIMessages.ACTION_CANCELLED

    def test_delete_contact_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(
            ValueError, match="delete-contact command requires 1 argument: name"
        ):
            contact_commands.delete_contact([], mock_service)


class TestShowPhone:
    """Tests for show_phone command."""

    @patch("src.application.commands.contact_commands._select_contact_by_name")
    def test_show_phone_success(self, mock_select, mock_service, sample_contact):
        """Test showing phone numbers successfully."""
        mock_select.return_value = sample_contact

        result = contact_commands.show_phone(["John Doe"], mock_service)

        assert "1234567890" in result

    @patch("src.application.commands.contact_commands._select_contact_by_name")
    def test_show_phone_no_phones(self, mock_select, mock_service):
        """Test showing phone when contact has no phones."""
        test_user = random_user()
        contact_no_phones = Contact(Name(test_user), "contact-456")
        mock_select.return_value = contact_no_phones

        result = contact_commands.show_phone([test_user], mock_service)

        assert "No phone numbers" in result or "no phone" in result.lower()

    def test_show_phone_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(
            ValueError, match="show-phone command requires 1 argument: name"
        ):
            contact_commands.show_phone([], mock_service)


class TestShowAll:
    """Tests for show_all command."""

    def test_show_all_with_contacts(self, mock_service, sample_contact):
        """Test showing all contacts when contacts exist."""
        mock_service.get_all_contacts.return_value = [sample_contact]

        result = contact_commands.show_all(mock_service)

        assert "John Doe" in result
        assert "1234567890" in result

    def test_show_all_no_contacts(self, mock_service):
        """Test showing all contacts when no contacts exist."""
        mock_service.get_all_contacts.return_value = []

        result = contact_commands.show_all(mock_service)

        assert "No contacts" in result


class TestAddBirthday:
    """Tests for add_birthday command."""

    @patch("src.application.commands.contact_commands._select_contact_by_name")
    def test_add_birthday_success(self, mock_select, mock_service, sample_contact):
        """Test adding a birthday successfully."""
        mock_select.return_value = sample_contact
        mock_service.add_birthday_by_id.return_value = "Birthday added."

        result = contact_commands.add_birthday(["John Doe", "01.01.1990"], mock_service)

        mock_service.add_birthday_by_id.assert_called_once()
        assert result == "Birthday added."

    def test_add_birthday_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(
            ValueError, match=r"Add-birthday command requires 2 arguments"
        ):
            contact_commands.add_birthday(["John Doe"], mock_service)


class TestShowBirthday:
    """Tests for show_birthday command."""

    @patch("src.application.commands.contact_commands._select_contact_by_name")
    def test_show_birthday_success(
        self, mock_select, mock_service, sample_contact_with_birthday
    ):
        """Test showing birthday successfully."""
        mock_select.return_value = sample_contact_with_birthday

        result = contact_commands.show_birthday(["John Doe"], mock_service)

        assert "01.01.1990" in result

    @patch("src.application.commands.contact_commands._select_contact_by_name")
    def test_show_birthday_no_birthday(self, mock_select, mock_service, sample_contact):
        """Test showing birthday when contact has no birthday."""
        mock_select.return_value = sample_contact

        result = contact_commands.show_birthday(["John Doe"], mock_service)

        assert "No birthday" in result or "not set" in result.lower()

    def test_show_birthday_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(
            ValueError, match="Show-birthday command requires 1 argument: name"
        ):
            contact_commands.show_birthday([], mock_service)


class TestBirthdays:
    """Tests for birthdays command."""

    def test_birthdays_default_days(self, mock_service):
        """Test getting upcoming birthdays with default days."""
        mock_service.get_upcoming_birthdays.return_value = []

        result = contact_commands.birthdays([], mock_service)

        mock_service.get_upcoming_birthdays.assert_called_once_with(7)
        assert "No upcoming birthdays" in result

    def test_birthdays_specified_days(self, mock_service):
        """Test getting upcoming birthdays with specified days."""
        mock_service.get_upcoming_birthdays.return_value = []

        result = contact_commands.birthdays(["30"], mock_service)

        mock_service.get_upcoming_birthdays.assert_called_once_with(30)

    def test_birthdays_no_upcoming(self, mock_service):
        """Test when there are no upcoming birthdays."""
        mock_service.get_upcoming_birthdays.return_value = []

        result = contact_commands.birthdays([], mock_service)

        assert "No upcoming birthdays" in result

    def test_birthdays_invalid_days_type(self, mock_service):
        """Test that invalid days type raises ValueError."""
        with pytest.raises(ValueError, match="Invalid amount of days ahead"):
            contact_commands.birthdays(["invalid"], mock_service)

    def test_birthdays_days_too_large(self, mock_service):
        """Test that days > 365 raises ValueError."""
        with pytest.raises(
            ValueError, match="Max amount of days for upcoming birthdays is 365"
        ):
            contact_commands.birthdays(["400"], mock_service)


class TestAddEmail:
    """Tests for add_email command."""

    @patch("src.application.commands.contact_commands._select_contact_by_name")
    def test_add_email_success(self, mock_select, mock_service, sample_contact):
        """Test adding email successfully."""
        mock_select.return_value = sample_contact
        mock_service.add_email_by_id.return_value = "Email added."

        result = contact_commands.add_email(
            ["John Doe", "john@example.com"], mock_service
        )

        mock_service.add_email_by_id.assert_called_once()
        assert result == "Email added."

    def test_add_email_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(ValueError, match="Add-email command requires 2 arguments"):
            contact_commands.add_email(["John Doe"], mock_service)


class TestRemoveEmail:
    """Tests for remove_email command."""

    @patch("src.application.commands.contact_commands.confirm_action")
    @patch("src.application.commands.contact_commands._select_contact_by_name")
    def test_remove_email_success(
        self, mock_select, mock_confirm, mock_service, sample_contact_with_email
    ):
        """Test removing email successfully."""
        mock_select.return_value = sample_contact_with_email
        mock_confirm.return_value = True
        mock_service.remove_email_by_id.return_value = "Email removed."

        result = contact_commands.remove_email(["John Doe"], mock_service)

        mock_confirm.assert_called_once()
        mock_service.remove_email_by_id.assert_called_once()
        assert result == "Email removed."

    @patch("src.application.commands.contact_commands.confirm_action")
    @patch("src.application.commands.contact_commands._select_contact_by_name")
    def test_remove_email_cancelled(
        self, mock_select, mock_confirm, mock_service, sample_contact_with_email
    ):
        """Test that cancelling remove email returns ACTION_CANCELLED."""
        mock_select.return_value = sample_contact_with_email
        mock_confirm.return_value = False

        result = contact_commands.remove_email(["John Doe"], mock_service)

        assert result == UIMessages.ACTION_CANCELLED
        mock_service.remove_email_by_id.assert_not_called()


class TestSelectContactByName:
    """Tests for _select_contact_by_name helper function."""

    @patch("src.application.commands.contact_commands.select_from_list")
    def test_select_single_contact(
        self, mock_select_list, mock_service, sample_contact
    ):
        """Test selecting when only one contact exists."""
        mock_service.find_all_by_name.return_value = [sample_contact]

        result = contact_commands._select_contact_by_name(mock_service, "John Doe")

        mock_select_list.assert_not_called()
        assert result == sample_contact

    @patch("src.application.commands.contact_commands.select_from_list")
    def test_select_multiple_contacts(
        self, mock_select_list, mock_service, sample_contact
    ):
        """Test selecting when multiple contacts exist."""
        # sample_contact =
        contact2 = Contact(Name("John Doe"), "contact-456")
        contact2.add_phone(Phone("9999999999"))

        mock_service.find_all_by_name.return_value = [sample_contact, contact2]
        mock_select_list.return_value = 0

        result = contact_commands._select_contact_by_name(mock_service, "John Doe")

        mock_select_list.assert_called_once()
        assert result == sample_contact

    def test_select_no_contacts(self, mock_service):
        """Test selecting when no contacts exist."""
        mock_service.find_all_by_name.return_value = []

        with pytest.raises(KeyError, match="Contact 'Nonexistent' not found"):
            contact_commands._select_contact_by_name(mock_service, "Nonexistent")
