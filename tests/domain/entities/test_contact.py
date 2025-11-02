import pytest
from unittest.mock import Mock
from src.domain.entities.contact import Contact
from src.domain.value_objects.name import Name
from src.domain.value_objects.phone import Phone
from src.domain.value_objects.email import Email
from src.domain.value_objects.address import Address
from src.domain.value_objects.birthday import Birthday


class TestContact:
    """Tests for the Contact entity."""

    @pytest.fixture
    def sample_contact(self):
        """Return a sample Contact instance for testing."""
        name = Name("John Doe")
        return Contact(name, "test-id-1")

    def test_contact_creation_success(self, sample_contact):
        """Test successful creation of a Contact."""
        assert sample_contact.name.value == "John Doe"
        assert sample_contact.id == "test-id-1"
        assert sample_contact.phones == []
        assert sample_contact.birthday is None
        assert sample_contact.email is None
        assert sample_contact.address is None

    def test_contact_creation_empty_id_raises_error(self):
        """Test that creating a contact with an empty ID raises ValueError."""
        with pytest.raises(ValueError, match="Contact ID is required"):
            Contact(Name("John Doe"), "")

    def test_create_classmethod(self):
        """Test the create classmethod for generating a contact with a new ID."""
        id_generator = Mock(return_value="new-unique-id")
        name = Name("Jane Doe")
        contact = Contact.create(name, id_generator)
        assert isinstance(contact, Contact)
        assert contact.id == "new-unique-id"
        assert contact.name == name
        id_generator.assert_called_once()

    def test_add_phone_success(self, sample_contact):
        """Test adding a new phone number."""
        phone = Phone("1234567890")
        sample_contact.add_phone(phone)
        assert len(sample_contact.phones) == 1
        assert phone in sample_contact.phones

    def test_add_duplicate_phone_raises_error(self, sample_contact):
        """Test that adding a duplicate phone number raises ValueError."""
        phone = Phone("1234567890")
        sample_contact.add_phone(phone)
        with pytest.raises(ValueError, match="Phone number already exists"):
            sample_contact.add_phone(phone)

    def test_find_phone_success(self, sample_contact):
        """Test finding an existing phone number."""
        phone = Phone("1234567890")
        sample_contact.add_phone(phone)
        found_phone = sample_contact.find_phone(phone)
        assert found_phone == phone

    def test_find_nonexistent_phone_raises_error(self, sample_contact):
        """Test that finding a non-existent phone number raises ValueError."""
        phone = Phone("1234567890")
        with pytest.raises(ValueError, match="Phone number not found"):
            sample_contact.find_phone(phone)

    def test_edit_phone_success(self, sample_contact):
        """Test successfully editing a phone number."""
        old_phone = Phone("1234567890")
        new_phone = Phone("0987654321")
        sample_contact.add_phone(old_phone)
        sample_contact.edit_phone(old_phone, new_phone)
        assert new_phone in sample_contact.phones
        assert old_phone not in sample_contact.phones

    def test_edit_phone_to_duplicate_raises_error(self, sample_contact):
        """Test that editing a phone to a number that already exists raises an error."""
        phone1 = Phone("1234567890")
        phone2 = Phone("0987654321")
        sample_contact.add_phone(phone1)
        sample_contact.add_phone(phone2)
        with pytest.raises(ValueError, match="New phone duplicates existing number"):
            sample_contact.edit_phone(phone1, phone2)

    def test_remove_phone_success(self, sample_contact):
        """Test successfully removing a phone number."""
        phone = Phone("1234567890")
        sample_contact.add_phone(phone)
        sample_contact.remove_phone(phone)
        assert len(sample_contact.phones) == 0

    def test_add_birthday(self, sample_contact):
        """Test adding a birthday."""
        birthday = Birthday("01.01.1990")
        sample_contact.add_birthday(birthday)
        assert sample_contact.birthday == birthday

    def test_add_email(self, sample_contact):
        """Test adding an email."""
        email = Email("john.doe@example.com")
        sample_contact.add_email(email)
        assert sample_contact.email == email

    def test_remove_email(self, sample_contact):
        """Test removing an email."""
        email = Email("john.doe@example.com")
        sample_contact.add_email(email)
        sample_contact.remove_email()
        assert sample_contact.email is None

    def test_add_address(self, sample_contact):
        """Test adding an address."""
        address = Address("123 Main St")
        sample_contact.add_address(address)
        assert sample_contact.address == address

    def test_remove_address(self, sample_contact):
        """Test removing an address."""
        address = Address("123 Main St")
        sample_contact.add_address(address)
        sample_contact.remove_address()
        assert sample_contact.address is None

    def test_is_matching_exact(self, sample_contact):
        """Test exact matching for search."""
        sample_contact.add_phone(Phone("1234567890"))
        sample_contact.add_email(Email("john.doe@example.com"))
        assert sample_contact.is_matching("John Doe", exact=True)
        assert sample_contact.is_matching("1234567890", exact=True)
        assert sample_contact.is_matching("john.doe@example.com", exact=True)
        assert not sample_contact.is_matching("John", exact=True)

    def test_is_matching_inexact(self, sample_contact):
        """Test case-insensitive, partial matching for search."""
        sample_contact.add_phone(Phone("1234567890"))
        sample_contact.add_email(Email("john.doe@example.com"))
        assert sample_contact.is_matching("john", exact=False)
        assert sample_contact.is_matching("123", exact=False)
        assert sample_contact.is_matching("DOE@EXAMPLE", exact=False)
        assert not sample_contact.is_matching("xyz", exact=False)

    def test_str_representation(self, sample_contact):
        """Test the string representation of a contact."""
        sample_contact.add_phone(Phone("1234567890"))
        sample_contact.add_birthday(Birthday("01.01.1990"))
        sample_contact.add_email(Email("john.doe@example.com"))
        sample_contact.add_address(Address("123 Main St"))
        expected = (
            "Contact name: John Doe, phones: 1234567890, "
            "birthday: 01.01.1990, "
            "email: john.doe@example.com, "
            "address: 123 Main St"
        )
        assert str(sample_contact) == expected

    def test_str_representation_minimal(self, sample_contact):
        """Test the string representation of a contact with minimal information."""
        expected = "Contact name: John Doe, phones: —"
        assert str(sample_contact) == expected
