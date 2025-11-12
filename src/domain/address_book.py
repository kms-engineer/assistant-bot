from collections import UserDict
from datetime import date, timedelta
from typing import Optional, Set

from .entities.contact import Contact
from .utils.birthday_utils import get_next_birthday_date, parse_date

DATE_FORMAT = "%d.%m.%Y"


class AddressBook(UserDict):

    def get_ids(self) -> Set[str]:
        return set(self.data.keys())

    def add_record(self, contact: Contact) -> None:
        key = contact.id
        if key in self.data:
            raise KeyError(f"Contact with ID '{key}' already exists")
        self.data[key] = contact

    def find(self, contact_name: str) -> Contact:
        for contact in self.data.values():
            if contact.name.value == contact_name:
                return contact
        raise KeyError("Contact not found")

    def find_all(self, contact_name: str) -> list[Contact]:
        matches = [
            contact
            for contact in self.data.values()
            if contact.name.value == contact_name
        ]
        return matches

    def find_by_id(self, contact_id: str) -> Optional[Contact]:
        return self.data.get(contact_id)

    def delete(self, contact_name: str) -> None:
        contact = self.find(contact_name)
        del self.data[contact.id]

    def delete_by_id(self, contact_id: str) -> None:
        if contact_id not in self.data:
            raise KeyError("Contact not found")
        del self.data[contact_id]

    def get_upcoming_birthdays(self, days_ahead) -> list[dict]:
        upcoming_birthdays = []
        today = date.today()
        next_n_days = today + timedelta(days=days_ahead)

        for contact in self.data.values():
            if contact.birthday is None:
                continue

            try:
                orig_birthday = parse_date(contact.birthday.value, DATE_FORMAT)
            except ValueError:
                continue

            try:
                next_birthday_date = get_next_birthday_date(orig_birthday, today)
            except ValueError:
                continue

            if today <= next_birthday_date <= next_n_days:
                upcoming_birthdays.append(
                    {
                        "name": contact.name.value,
                        "birthdays_date": next_birthday_date.strftime(DATE_FORMAT),
                    }
                )

        return upcoming_birthdays
