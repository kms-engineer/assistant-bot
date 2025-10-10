from typing import Optional

from ...domain.address_book import AddressBook
from ...domain.entities.contact import Contact
from ...domain.utils.id_generator import IDGenerator
from ...infrastructure.persistence.data_path_resolver import DEFAULT_CONTACTS_FILE
from ...infrastructure.persistence.domain_storage_adapter import DomainStorageAdapter
from ...infrastructure.serialization.json_serializer import JsonSerializer
from ...infrastructure.storage.pickle_storage import PickleStorage
from ...infrastructure.storage.storage_interface import StorageInterface


class ContactService:

    def __init__(self, storage: StorageInterface = None, serializer: JsonSerializer = None):
        raw_storage = storage if storage else PickleStorage()
        self.storage = DomainStorageAdapter(raw_storage, serializer)
        self.address_book = AddressBook()
        self._current_filename = DEFAULT_CONTACTS_FILE

    def load_address_book(self, filename: str = DEFAULT_CONTACTS_FILE, user_provided: bool = False) -> int:
        loaded_book, normalized_filename = self.storage.load_contacts(
            filename,
            user_provided=user_provided
        )

        self.address_book = loaded_book if loaded_book else AddressBook()
        self._current_filename = normalized_filename

        return len(self.address_book.data)

    def save_address_book(self, filename: Optional[str] = None, user_provided: bool = False) -> str:
        target = filename if filename else self._current_filename

        saved_filename = self.storage.save_contacts(
            self.address_book,
            target,
            user_provided=user_provided
        )
        self._current_filename = saved_filename
        return saved_filename

    def add_contact(self, name: str, phone: str) -> str:
        try:
            contact = self.address_book.find(name)
            contact.add_phone(phone)
            return "Contact updated."
        except KeyError:
            contact = Contact.create(
                name,
                lambda: IDGenerator.generate_unique_id(
                    lambda: self.address_book.get_ids()
                )
            )
            contact.add_phone(phone)
            self.address_book.add_record(contact)
            return "Contact added."

    def change_phone(self, name: str, old_phone: str, new_phone: str) -> str:
        contact = self.address_book.find(name)
        contact.edit_phone(old_phone, new_phone)
        return "Contact phone number updated."

    def delete_contact(self, name: str) -> str:
        self.address_book.delete(name)
        return "Contact deleted."

    def get_phones(self, name: str) -> list[str]:
        contact = self.address_book.find(name)
        return [phone.value for phone in contact.phones]

    def get_all_contacts(self) -> list[Contact]:
        return list(self.address_book.data.values())

    def add_birthday(self, name: str, birthday: str) -> str:
        contact = self.address_book.find(name)
        contact.add_birthday(birthday)
        return f"Birthday added for {name}."

    def get_birthday(self, name: str) -> Optional[str]:
        contact = self.address_book.find(name)
        return contact.birthday.value if contact.birthday else None

    def get_upcoming_birthdays(self, days_ahead) -> list[dict]:
        return self.address_book.get_upcoming_birthdays(days_ahead)

    def add_email(self, name: str, email: str) -> str:
        contact = self.address_book.find(name)
        contact.add_email(email)
        return f"Email added for {name}."

    def add_address(self, name: str, address: str) -> str:
        contact = self.address_book.find(name)
        contact.add_address(address)
        return f"Address added for {name}."

    def get_current_filename(self) -> str:
        return self._current_filename
