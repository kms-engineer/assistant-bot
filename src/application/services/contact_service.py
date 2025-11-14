from typing import Optional

from src.domain.address_book import AddressBook
from src.domain.entities.contact import Contact
from src.domain.utils.id_generator import IDGenerator
from src.domain.value_objects.address import Address
from src.domain.value_objects.birthday import Birthday
from src.domain.value_objects.email import Email
from src.domain.value_objects.name import Name
from src.domain.value_objects.phone import Phone
from src.infrastructure.persistence.data_path_resolver import DEFAULT_CONTACTS_FILE
from src.infrastructure.persistence.domain_storage_adapter import DomainStorageAdapter
from src.infrastructure.serialization.json_serializer import JsonSerializer
from src.infrastructure.storage.pickle_storage import PickleStorage
from src.infrastructure.storage.storage import Storage


class ContactService:

    def __init__(
        self,
        storage: Optional[Storage] = None,
        serializer: Optional[JsonSerializer] = None,
    ):
        raw_storage = storage if storage else PickleStorage()
        self.storage = DomainStorageAdapter(raw_storage, serializer)
        self.address_book = AddressBook()
        self._current_filename = DEFAULT_CONTACTS_FILE

    def load_address_book(
        self, filename: str | None = DEFAULT_CONTACTS_FILE, user_provided: bool = False
    ) -> int:
        loaded_book, normalized_filename = self.storage.load_contacts(
            filename, user_provided=user_provided
        )

        self.address_book = loaded_book if loaded_book else AddressBook()
        self._current_filename = normalized_filename

        return len(self.address_book.data)

    def save_address_book(
        self, filename: Optional[str] = None, user_provided: bool = False
    ) -> str:
        target = filename if filename else self._current_filename

        saved_filename = self.storage.save_contacts(
            self.address_book, target, user_provided=user_provided
        )
        self._current_filename = saved_filename
        return saved_filename

    def add_contact(self, name: Name, phone: Phone) -> str:
        try:
            # Try to find existing contact
            contact = self.address_book.find(name.value)
            try:
                contact.add_phone(phone)
                return f"Phone number {phone.value} added to existing contact {name.value}."
            except ValueError as e:
                # Phone already exists for this contact
                if "already exists" in str(e):
                    return (
                        f"Phone number {phone.value} already exists for {name.value}."
                    )
                raise  # Re-raise if it's a different ValueError
        except KeyError:
            # Contact doesn't exist, create new one
            contact = Contact.create(
                name,
                lambda: IDGenerator.generate_unique_id(
                    lambda: self.address_book.get_ids()
                ),
            )
            contact.add_phone(phone)
            self.address_book.add_record(contact)
            return f"Contact {name.value} added with phone {phone.value}."

    def change_phone(self, name: str, old_phone: Phone, new_phone: Phone) -> str:
        contact = self.address_book.find(name)
        contact.edit_phone(old_phone, new_phone)
        return "Contact phone number updated."

    def edit_phone_by_id(
        self, contact_id: str, old_phone: Phone, new_phone: Phone
    ) -> str:
        contact = self.address_book.find_by_id(contact_id)
        if not contact:
            raise KeyError(f"Contact with ID {contact_id} not found")
        contact.edit_phone(old_phone, new_phone)
        return "Contact phone number updated."

    def remove_phone_by_id(self, contact_id: str, phone: Phone) -> str:
        contact = self.address_book.find_by_id(contact_id)
        if not contact:
            raise KeyError(f"Contact with ID {contact_id} not found")
        if len(contact.phones) == 1:
            raise ValueError(
                f"Cannot remove the only phone number. Contact must have at least one phone."
            )
        contact.remove_phone(phone)
        return f"Phone number {phone.value} removed from {contact.name.value}."

    def remove_phone(self, name: str, phone: Phone) -> str:
        contact = self.address_book.find(name)
        if len(contact.phones) == 1:
            raise ValueError(
                f"Cannot remove the only phone number. Contact must have at least one phone."
            )
        contact.remove_phone(phone)
        return f"Phone number {phone.value} removed from {name}."

    def delete_contact(self, name: str) -> str:
        self.address_book.delete(name)
        return "Contact deleted."

    def delete_contact_by_id(self, contact_id: str) -> str:
        self.address_book.delete_by_id(contact_id)
        return "Contact deleted."

    def find_all_by_name(self, name: str) -> list[Contact]:
        return self.address_book.find_all(name)

    def add_phone_to_contact(self, contact_id: str, phone: Phone) -> str:
        contact = self.address_book.find_by_id(contact_id)
        if not contact:
            raise KeyError(f"Contact with ID {contact_id} not found")

        try:
            contact.add_phone(phone)
            return f"Phone number {phone.value} added to existing contact {contact.name.value}."
        except ValueError as e:
            if "already exists" in str(e):
                return f"Phone number {phone.value} already exists for {contact.name.value}."
            raise

    def create_new_contact(self, name: Name, phone: Phone) -> str:
        contact = Contact.create(
            name,
            lambda: IDGenerator.generate_unique_id(lambda: self.address_book.get_ids()),
        )
        contact.add_phone(phone)
        self.address_book.add_record(contact)
        return f"New contact {name.value} created with phone {phone.value}."

    def get_phones(self, name: str) -> list[str]:
        contact = self.address_book.find(name)
        return [phone.value for phone in contact.phones]

    def get_all_contacts(self) -> list[Contact]:
        return list(self.address_book.data.values())

    def add_birthday_by_id(self, contact_id: str, birthday: Birthday) -> str:
        contact = self.address_book.find_by_id(contact_id)
        if not contact:
            raise KeyError(f"Contact with ID {contact_id} not found")
        contact.add_birthday(birthday)
        return f"Birthday added for {contact.name.value}."

    def add_birthday(self, name: str, birthday: Birthday) -> str:
        contact = self.address_book.find(name)
        contact.add_birthday(birthday)
        return f"Birthday added for {name}."

    def get_birthday(self, name: str) -> Optional[str]:
        contact = self.address_book.find(name)
        return contact.birthday.value if contact.birthday else None

    def get_upcoming_birthdays(self, days_ahead) -> list[dict]:
        return self.address_book.get_upcoming_birthdays(days_ahead)

    def remove_birthday_by_id(self, contact_id: str) -> str:
        contact = self.address_book.find_by_id(contact_id)
        if not contact:
            raise KeyError(f"Contact with ID {contact_id} not found")
        birthday = contact.birthday
        if contact.birthday:
            contact.remove_birthday()
            return f"Birthday {birthday} removed from {contact.name.value}."
        else:
            return f"{contact.name.value} has no birthday set."

    def remove_birthday(self, name: str) -> str:
        contact = self.address_book.find(name)
        birthday = contact.birthday
        if contact.birthday:
            contact.remove_birthday()
            return f"Birthday {birthday} removed from {name}."
        else:
            return f"{name} has no birthday set."

    def add_email_by_id(self, contact_id: str, email: Email) -> str:
        contact = self.address_book.find_by_id(contact_id)
        if not contact:
            raise KeyError(f"Contact with ID {contact_id} not found")
        contact.add_email(email)
        return f"Email added for {contact.name.value}."

    def edit_email_by_id(self, contact_id: str, email: Email) -> str:
        contact = self.address_book.find_by_id(contact_id)
        if not contact:
            raise KeyError(f"Contact with ID {contact_id} not found")
        if contact.email:
            contact.remove_email()
            contact.add_email(email)
            return f"New email is set for {contact.name.value}"
        else:
            contact.add_email(email)
            return f"Email added for {contact.name.value}."

    def remove_email_by_id(self, contact_id: str) -> str:
        contact = self.address_book.find_by_id(contact_id)
        if not contact:
            raise KeyError(f"Contact with ID {contact_id} not found")
        email = contact.email
        if contact.email:
            contact.remove_email()
            return f"Email {email} from {contact.name.value} removed successfully"
        else:
            raise ValueError(
                f"Can't remove email for {contact.name.value}.\nEmail is not set yet."
            )

    def add_email(self, name: str, email: Email) -> str:
        contact = self.address_book.find(name)
        contact.add_email(email)
        return f"Email added for {name}."

    def edit_email(self, name: str, email: Email) -> str:
        contact = self.address_book.find(name)
        if contact.email:
            # I keep it in method due to security and scaling reasons
            # We could add some extra logic in remove_email later
            # There is no need to have email edit, remove and add methods in Contact\
            # We could just reuse add and remove method here
            contact.remove_email()
            contact.add_email(email)
            return f"New email is set for {name}"
        else:
            return self.add_email(name, email)

    def remove_email(self, name: str) -> str:
        contact = self.address_book.find(name)
        email = contact.email
        if contact.email:
            contact.remove_email()
            return f"Email {email} from {name} removed successfully"
        else:
            raise ValueError(f"Can't remove email for {name}.\nEmail is not set yet.")

    def add_address_by_id(self, contact_id: str, address: Address) -> str:
        contact = self.address_book.find_by_id(contact_id)
        if not contact:
            raise KeyError(f"Contact with ID {contact_id} not found")
        contact.add_address(address)
        return f"Address added for {contact.name.value}."

    def edit_address_by_id(self, contact_id: str, address: Address) -> str:
        contact = self.address_book.find_by_id(contact_id)
        if not contact:
            raise KeyError(f"Contact with ID {contact_id} not found")
        if contact.address:
            contact.remove_address()
            contact.add_address(address)
            return f"New address is set for {contact.name.value}"
        else:
            contact.add_address(address)
            return f"Address added for {contact.name.value}."

    def remove_address_by_id(self, contact_id: str) -> str:
        contact = self.address_book.find_by_id(contact_id)
        if not contact:
            raise KeyError(f"Contact with ID {contact_id} not found")
        address = contact.address
        if contact.address:
            contact.remove_address()
            return f"Address {address} from {contact.name.value} removed successfully"
        else:
            raise ValueError(
                f"Can't remove address for {contact.name.value}.\nAddress is not set yet."
            )

    def add_address(self, name: str, address: Address) -> str:
        contact = self.address_book.find(name)
        contact.add_address(address)
        return f"Address added for {name}."

    def edit_address(self, name: str, address: Address):
        contact = self.address_book.find(name)
        if contact.address:
            contact.remove_address()
            contact.add_address(address)
            return f"New address is set for {name}"
        else:
            return self.add_address(name, address)

    def remove_address(self, name: str) -> str:
        contact = self.address_book.find(name)
        address = contact.address
        if contact.address:
            contact.remove_address()
            return f"Address {address} from {name} removed successfully"
        else:
            raise ValueError(
                f"Can't remove address for {name}.\nAddress is not set yet."
            )

    def search(self, search_text: str, exact=False) -> list[Contact]:
        return list(
            filter(
                lambda c: c.is_matching(search_text, exact), self.address_book.values()
            )
        )

    def get_current_filename(self) -> str:
        return self._current_filename
