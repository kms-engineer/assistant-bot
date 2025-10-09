from collections import UserDict
from typing import Optional, Set
from datetime import datetime, timedelta
from .entities.contact import Contact
from .utils.birthday_utils import get_birthday_for_year, move_to_monday_if_weekend

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

    def find_by_id(self, contact_id: str) -> Optional[Contact]:
        return self.data.get(contact_id)

    def delete(self, contact_name: str) -> None:
        contact = self.find(contact_name)
        del self.data[contact.id]

    def delete_by_id(self, contact_id: str) -> None:
        if contact_id not in self.data:
            raise KeyError("Contact not found")
        del self.data[contact_id]

    def get_upcoming_birthdays(self) -> list[dict]:
        upcoming_birthdays = []
        today = datetime.today().date()

        for contact in self.data.values():
            if contact.birthday is None:
                continue

            try:
                orig_birthday = datetime.strptime(contact.birthday.value, DATE_FORMAT).date()
            except ValueError:
                continue

            try:
                congratulation_date = get_birthday_for_year(orig_birthday, today.year)
                if congratulation_date < today:
                    congratulation_date = get_birthday_for_year(orig_birthday, today.year + 1)
            except ValueError:
                continue

            next_7days = today + timedelta(days=7)
            if today <= congratulation_date <= next_7days:
                congratulation_date = move_to_monday_if_weekend(congratulation_date)
                upcoming_birthdays.append({
                    "name": contact.name.value,
                    "congratulation_date": congratulation_date.strftime(DATE_FORMAT)
                })

        return upcoming_birthdays
