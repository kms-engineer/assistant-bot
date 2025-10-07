from typing import Optional
from ...domain.address_book import AddressBook
from ...domain.entities.contact import Contact
from ...infrastructure.storage.storage import Storage
from ...infrastructure.storage.pickle_storage import PickleStorage
from ...infrastructure.serialization.json_serializer import JsonSerializer
from ...infrastructure.persistence.data_path_resolver import DEFAULT_CONTACTS_FILE
from ...infrastructure.persistence.domain_storage_adapter import DomainStorageAdapter


class ContactService:

    def __init__(self, storage: Storage = None, serializer: JsonSerializer = None):
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
            record = self.address_book.find(name)
            record.add_phone(phone)
            return "Contact updated."
        except KeyError:
            record = Contact(name)
            record.add_phone(phone)
            self.address_book.add_record(record)
            return "Contact added."

    def change_phone(self, name: str, old_phone: str, new_phone: str) -> str:
        record = self.address_book.find(name)
        record.edit_phone(old_phone, new_phone)
        return "Contact phone number updated."

    def get_phones(self, name: str) -> list[str]:
        record = self.address_book.find(name)
        return [phone.value for phone in record.phones]

    def get_all_contacts(self) -> list[Contact]:
        return list(self.address_book.data.values())

    def add_birthday(self, name: str, birthday: str) -> str:
        record = self.address_book.find(name)
        record.add_birthday(birthday)
        return f"Birthday added for {name}."

    def get_birthday(self, name: str) -> Optional[str]:
        record = self.address_book.find(name)
        return record.birthday.value if record.birthday else None

    def get_upcoming_birthdays(self) -> list[dict]:
        return self.address_book.get_upcoming_birthdays()

    def add_email(self, name: str, email: str) -> str:
        record = self.address_book.find(name)
        record.add_email(email)
        return f"Email added for {name}."

    def add_address(self, name: str, address: str) -> str:
        record = self.address_book.find(name)
        record.add_address(address)
        return f"Address added for {name}."

    def get_current_filename(self) -> str:
        return self._current_filename
