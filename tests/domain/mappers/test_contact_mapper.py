import pytest
from src.domain.mappers.contact_mapper import ContactMapper
from src.domain.entities.contact import Contact
from src.domain.models.dbcontact import DBContact
from src.domain.value_objects.name import Name
from src.domain.value_objects.phone import Phone
from src.domain.value_objects.email import Email
from src.domain.value_objects.address import Address
from src.domain.value_objects.birthday import Birthday


class TestContactMapper:
    """Tests for the ContactMapper class."""

    def test_to_dbmodel_full(self):
        """Test mapping a full Contact entity to a DBContact model."""
        contact = Contact(Name("John Doe"), contact_id="test-id")
        contact.add_phone(Phone("1234567890"))
        contact.add_phone(Phone("0987654321"))
        contact.add_birthday(Birthday("01.01.1990"))
        contact.add_email(Email("john.doe@example.com"))
        contact.add_address(Address("123 Main St"))

        db_contact = ContactMapper.to_dbmodel(contact)

        assert isinstance(db_contact, DBContact)
        assert db_contact.id == "test-id"
        assert db_contact.name == "John Doe"
        assert db_contact.phones == "1234567890,0987654321"
        assert db_contact.birthday == "01.01.1990"
        assert db_contact.email == "john.doe@example.com"
        assert db_contact.address == "123 Main St"

    def test_to_dbmodel_minimal(self):
        """Test mapping a minimal Contact entity (only name) to a DBContact model."""
        contact = Contact(Name("Jane Doe"), contact_id="test-id-2")

        db_contact = ContactMapper.to_dbmodel(contact)

        assert isinstance(db_contact, DBContact)
        assert db_contact.id == "test-id-2"
        assert db_contact.name == "Jane Doe"
        assert db_contact.phones == ""
        assert db_contact.birthday is None
        assert db_contact.email is None
        assert db_contact.address is None

    def test_from_dbmodel_full(self):
        """Test mapping a full DBContact model to a Contact entity."""
        db_contact = DBContact(
            id="test-id",
            name="John Doe",
            phones="1234567890,0987654321",
            birthday="01.01.1990",
            email="john.doe@example.com",
            address="123 Main St",
        )

        contact = ContactMapper.from_dbmodel(db_contact)

        assert isinstance(contact, Contact)
        assert contact.id == "test-id"
        assert contact.name.value == "John Doe"
        assert len(contact.phones) == 2
        assert Phone("1234567890") in contact.phones
        assert Phone("0987654321") in contact.phones
        assert contact.birthday.value == "01.01.1990"
        assert contact.email.value == "john.doe@example.com"
        assert contact.address.value == "123 Main St"

    def test_from_dbmodel_minimal(self):
        """Test mapping a minimal DBContact model (only name and id) to a Contact entity."""
        db_contact = DBContact(
            id="test-id-2",
            name="Jane Doe",
            phones=None,
            birthday=None,
            email=None,
            address=None,
        )

        contact = ContactMapper.from_dbmodel(db_contact)

        assert isinstance(contact, Contact)
        assert contact.id == "test-id-2"
        assert contact.name.value == "Jane Doe"
        assert len(contact.phones) == 0
        assert contact.birthday is None
        assert contact.email is None
        assert contact.address is None
