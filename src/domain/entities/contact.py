from typing import Optional, Callable

from src.domain.entities.entity import Entity
from src.domain.value_objects.address import Address
from src.domain.value_objects.birthday import Birthday
from src.domain.value_objects.email import Email
from src.domain.value_objects.name import Name
from src.domain.value_objects.phone import Phone


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
    def create(cls, name: Name, id_generator: Callable[[], str]) -> "Contact":
        contact_id = id_generator()
        return cls(name, contact_id)

    def add_phone(self, phone: Phone) -> None:
        if phone in self.phones:
            raise ValueError("Phone number already exists")
        self.phones.append(phone)

    def find_phone(self, phone: Phone) -> Phone:
        for p in self.phones:
            if p.value == phone.value:
                return p
        raise ValueError("Phone number not found")

    def edit_phone(self, old_phone: Phone, new_phone: Phone) -> None:
        current = self.find_phone(old_phone)
        if new_phone in self.phones and new_phone != current:
            raise ValueError("New phone duplicates existing number")
        idx = self.phones.index(current)
        self.phones[idx] = new_phone

    def remove_phone(self, phone: Phone) -> None:
        p = self.find_phone(phone)
        self.phones.remove(p)

    def add_birthday(self, birthday: Birthday) -> None:
        self.birthday = birthday

    def remove_birthday(self) -> None:
        self.birthday = None

    def add_email(self, email: Email) -> None:
        self.email = email

    def remove_email(self) -> None:
        self.email = None

    def remove_address(self) -> None:
        self.address = None

    def add_address(self, address: Address) -> None:
        self.address = address

    def is_matching(self, search_text: str, exact: bool) -> bool:
        # Collect all searchable field values
        values = [str(self.name)]
        if self.email:
            values.append(str(self.email))
        if self.address:
            values.append(str(self.address))
        values.extend(str(phone) for phone in self.phones)

        # Normalize search text for phone number comparison (remove all non-digits)
        search_normalized = ''.join(c for c in search_text if c.isdigit())

        # Check if search text looks like a phone number (contains digits)
        if search_normalized:
            # Check against normalized phone values
            for phone in self.phones:
                # Phone.value already contains normalized digits only
                if search_normalized in phone.value or phone.value in search_normalized:
                    return True

        # Perform search
        if exact:
            return search_text in values

        search_lower = search_text.casefold()
        return any(search_lower in val.casefold() for val in values)

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
