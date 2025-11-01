import pytest
from unittest.mock import Mock, patch
from src.application.services.contact_service import ContactService
from src.domain.entities.contact import Contact
from src.domain.value_objects.name import Name
from src.domain.value_objects.phone import Phone
from src.domain.value_objects.email import Email
from src.domain.value_objects.address import Address
from src.domain.value_objects.birthday import Birthday
from src.domain.address_book import AddressBook


@pytest.fixture
def mock_storage():
    """Create a mock storage for testing."""
    return Mock()


@pytest.fixture
def contact_service(mock_storage):
    """Create a ContactService with mock storage."""
    with patch('src.application.services.contact_service.DomainStorageAdapter') as mock_adapter:
        mock_adapter.return_value = mock_storage
        service = ContactService(storage=mock_storage)
        return service


@pytest.fixture
def sample_contact(contact_service):
    """Create a sample contact for testing."""
    name = Name("John Doe")
    phone = Phone("1234567890")
    contact_service.add_contact(name, phone)
    return contact_service.address_book.find("John Doe")


class TestContactService:
    """Tests for the ContactService class."""

    def test_add_new_contact(self, contact_service):
        """Test adding a completely new contact."""
        name = Name("Jane Doe")
        phone = Phone("9876543210")
        result = contact_service.add_contact(name, phone)
        assert "Contact Jane Doe added" in result
        assert len(contact_service.address_book.data) == 1

    def test_add_phone_to_existing_contact(self, contact_service, sample_contact):
        """Test adding a new phone number to an existing contact."""
        new_phone = Phone("1112223333")
        result = contact_service.add_contact(Name("John Doe"), new_phone)
        assert "Phone number 1112223333 added" in result
        assert len(sample_contact.phones) == 2

    def test_add_existing_phone_to_contact(self, contact_service, sample_contact):
        """Test adding a phone number that already exists for a contact."""
        existing_phone = Phone("1234567890")
        result = contact_service.add_contact(Name("John Doe"), existing_phone)
        assert "Phone number 1234567890 already exists" in result
        assert len(sample_contact.phones) == 1

    def test_change_phone_success(self, contact_service, sample_contact):
        """Test changing a contact's phone number."""
        old_phone = Phone("1234567890")
        new_phone = Phone("0987654321")
        result = contact_service.change_phone("John Doe", old_phone, new_phone)
        assert result == "Contact phone number updated."
        assert new_phone in sample_contact.phones
        assert old_phone not in sample_contact.phones

    def test_delete_contact_success(self, contact_service, sample_contact):
        """Test deleting a contact."""
        result = contact_service.delete_contact("John Doe")
        assert result == "Contact deleted."
        with pytest.raises(KeyError):
            contact_service.address_book.find("John Doe")

    def test_get_phones_success(self, contact_service, sample_contact):
        """Test getting a contact's phone numbers."""
        phones = contact_service.get_phones("John Doe")
        assert len(phones) == 1
        assert "1234567890" in phones

    def test_get_all_contacts(self, contact_service, sample_contact):
        """Test getting all contacts."""
        contacts = contact_service.get_all_contacts()
        assert len(contacts) == 1
        assert sample_contact in contacts

    def test_add_birthday_success(self, contact_service, sample_contact):
        """Test adding a birthday to a contact."""
        birthday = Birthday("01.01.1990")
        result = contact_service.add_birthday("John Doe", birthday)
        assert result == "Birthday added for John Doe."
        assert sample_contact.birthday == birthday

    def test_get_birthday_success(self, contact_service, sample_contact):
        """Test getting a contact's birthday."""
        birthday = Birthday("01.01.1990")
        contact_service.add_birthday("John Doe", birthday)
        result = contact_service.get_birthday("John Doe")
        assert result == "01.01.1990"

    def test_get_upcoming_birthdays(self, contact_service):
        """Test getting upcoming birthdays."""
        with patch.object(contact_service.address_book, 'get_upcoming_birthdays') as mock_get_birthdays:
            mock_get_birthdays.return_value = [{"name": "John Doe", "birthday": "2024-12-25"}]
            result = contact_service.get_upcoming_birthdays(10)
            mock_get_birthdays.assert_called_once_with(10)
            assert len(result) == 1
            assert result[0]["name"] == "John Doe"

    def test_add_email_success(self, contact_service, sample_contact):
        """Test adding an email to a contact."""
        email = Email("john.doe@example.com")
        result = contact_service.add_email("John Doe", email)
        assert result == "Email added for John Doe."
        assert sample_contact.email == email

    def test_edit_email_success(self, contact_service, sample_contact):
        """Test editing a contact's email."""
        contact_service.add_email("John Doe", Email("initial@example.com"))
        new_email = Email("updated@example.com")
        result = contact_service.edit_email("John Doe", new_email)
        assert result == "New email is set for John Doe"
        assert sample_contact.email == new_email

    def test_remove_email_success(self, contact_service, sample_contact):
        """Test removing an email from a contact."""
        email = Email("john.doe@example.com")
        contact_service.add_email("John Doe", email)
        result = contact_service.remove_email("John Doe")
        assert "Email john.doe@example.com from John Doe removed successfully" in result
        assert sample_contact.email is None

    def test_remove_email_not_set(self, contact_service, sample_contact):
        """Test removing an email when none is set."""
        with pytest.raises(ValueError, match="Can't remove email for John Doe.\nEmail is not set yet."):
            contact_service.remove_email("John Doe")

    def test_add_address_success(self, contact_service, sample_contact):
        """Test adding an address to a contact."""
        address = Address("123 Main St")
        result = contact_service.add_address("John Doe", address)
        assert result == "Address added for John Doe."
        assert sample_contact.address == address

    def test_edit_address_success(self, contact_service, sample_contact):
        """Test editing a contact's address."""
        contact_service.add_address("John Doe", Address("Initial Address"))
        new_address = Address("Updated Address")
        result = contact_service.edit_address("John Doe", new_address)
        assert result == "New address is set for John Doe"
        assert sample_contact.address == new_address

    def test_remove_address_success(self, contact_service, sample_contact):
        """Test removing an address from a contact."""
        address = Address("123 Main St")
        contact_service.add_address("John Doe", address)
        result = contact_service.remove_address("John Doe")
        assert "Address 123 Main St from John Doe removed successfully" in result
        assert sample_contact.address is None

    def test_remove_address_not_set(self, contact_service, sample_contact):
        """Test removing an address when none is set."""
        with pytest.raises(ValueError, match="Can't remove address for John Doe.\nAddress is not set yet."):
            contact_service.remove_address("John Doe")

    def test_search_exact(self, contact_service, sample_contact):
        """Test exact search for a contact."""
        results = contact_service.search("John Doe", exact=True)
        assert len(results) == 1
        assert results[0].name.value == "John Doe"

    def test_search_inexact(self, contact_service, sample_contact):
        """Test inexact search for a contact."""
        results = contact_service.search("john")
        assert len(results) == 1
        assert results[0].name.value == "John Doe"

    def test_load_address_book(self, contact_service, mock_storage):
        """Test loading an address book from storage."""
        mock_address_book = AddressBook()
        mock_address_book.add_record(Contact.create(Name("Loaded Contact"), lambda: "1"))
        mock_storage.load_contacts.return_value = (mock_address_book, "loaded.pkl")
        count = contact_service.load_address_book("loaded.pkl")
        assert count == 1
        assert len(contact_service.address_book.data) == 1
        assert contact_service.get_current_filename() == "loaded.pkl"

    def test_save_address_book(self, contact_service, mock_storage):
        """Test saving an address book to storage."""
        mock_storage.save_contacts.return_value = "saved.pkl"
        filename = contact_service.save_address_book("saved.pkl")
        mock_storage.save_contacts.assert_called_once_with(contact_service.address_book, "saved.pkl", user_provided=False)
        assert filename == "saved.pkl"
        assert contact_service.get_current_filename() == "saved.pkl"
