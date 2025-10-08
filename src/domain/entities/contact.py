import uuid
from typing import Optional

from .entity import Entity
from ..validators.phone_validator import PhoneValidator
from ..value_objects.name import Name
from ..value_objects.phone import Phone
from ..value_objects.birthday import Birthday
from ..value_objects.email import Email
from ..value_objects.address import Address


class Contact(Entity):

    def __init__(self, name: str, contact_id: Optional[str] = None):
        self.id = contact_id if contact_id else str(uuid.uuid4())
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Optional[Birthday] = None
        self.email: Optional[Email] = None
        self.address: Optional[Address] = None

    def add_phone(self, phone: str) -> None:
        phone_obj = Phone(phone)
        if phone_obj in self.phones:
            raise ValueError("Phone number already exists")
        self.phones.append(phone_obj)

    def find_phone(self, phone: str) -> Phone:
        norm = PhoneValidator.normalize(phone)
        for p in self.phones:
            if p.value == norm:
                return p
        raise ValueError("Phone number not found")

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        current = self.find_phone(old_phone)
        new_obj = Phone(new_phone)
        if new_obj in self.phones and new_obj != current:
            raise ValueError("New phone duplicates existing number")
        idx = self.phones.index(current)
        self.phones[idx] = new_obj

    def remove_phone(self, phone: str) -> None:
        p = self.find_phone(phone)
        self.phones.remove(p)

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def add_email(self, email: str) -> None:
        self.email = Email(email)

    def add_address(self, address: str) -> None:
        self.address = Address(address)

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
