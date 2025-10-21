import uuid
from typing import Optional, Callable

from .entity import Entity
from ..value_objects.name import Name
from ..value_objects.phone import Phone
from ..value_objects.address import Address
from ..value_objects.birthday import Birthday
from ..value_objects.email import Email


class Contact(Entity):

    def __init__(self, name: Name, contact_id: str):
        if not contact_id:
            raise ValueError("Contact ID is required")
        self.id = contact_id
        self.name = name
        self.phones: list[Phone] = []
        self.birthday: Optional[Birthday] = None
        self.email: Optional[Email] = None
        self.address: Optional[Address] = None

    @classmethod
    def create(cls, name: Name, id_generator: Callable[[], str]) -> 'Contact':
        contact_id = id_generator()
        return cls(name, contact_id)

    def add_phone(self, phone: Phone) -> None:
        if phone in self.phones:
            raise ValueError("Phone number already exists")
        self.phones.append(phone)

    def find_phone(self, phone: Phone) -> Phone:
        """Find phone by Phone VO."""
        for p in self.phones:
            if p.value == phone.value:
                return p
        raise ValueError("Phone number not found")

    def edit_phone(self, old_phone: Phone, new_phone: Phone) -> None:
        """Edit phone. Both parameters must be Phone VOs."""
        current = self.find_phone(old_phone)
        if new_phone in self.phones and new_phone != current:
            raise ValueError("New phone duplicates existing number")
        idx = self.phones.index(current)
        self.phones[idx] = new_phone

    def remove_phone(self, phone: Phone) -> None:
        """Remove phone by Phone VO."""
        p = self.find_phone(phone)
        self.phones.remove(p)

    def add_birthday(self, birthday: Birthday) -> None:
        self.birthday = birthday

    def add_email(self, email: Email) -> None:
        self.email = email

    def remove_email(self) -> None:
        self.email = None

    def remove_address(self) -> None:
        self.address = None

    def add_address(self, address: Address) -> None:
        self.address = address

    def is_matching(self, search_text: str, exact: bool) -> bool:
        if exact:
            return search_text == str(self.name) or search_text == str(self.email) or any(
                search_text == str(phone) for phone in self.phones)
        else:
            return search_text.casefold() in str(self.name).casefold() or \
                   search_text.casefold() in str(self.email).casefold() or \
                   any(search_text.casefold() in str(phone).casefold() for phone in self.phones)

    def __str__(self) -> str:
        phones_str = "; ".join(p.value for p in self.phones) or "—"
        parts = [f"Contact name: {self.name.value}, phones: {phones_str}"]

        if self.birthday:
            parts.append(f"birthday: {self.birthday}")
        if self.email:
            parts.append(f"email: {self.email}")
        if self.address:
            parts.append(f"address: {self.address}")

        return ", ".join(parts)
