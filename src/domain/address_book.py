from collections import UserDict
from typing import Optional
from datetime import datetime, timedelta
from .entities.contact import Contact
from .utils.birthday_utils import get_birthday_for_year, move_to_monday_if_weekend


DATE_FORMAT = "%d.%m.%Y"


class AddressBook(UserDict):

    def add_record(self, record: Contact) -> None:
        key = record.id
        if key in self.data:
            raise KeyError(f"Record with ID '{key}' already exists")
        self.data[key] = record

    def find(self, contact_name: str) -> Contact:
        for record in self.data.values():
            if record.name.value == contact_name:
                return record
        raise KeyError("Contact not found")

    def find_by_id(self, record_id: str) -> Optional[Contact]:
        return self.data.get(record_id)

    def delete(self, contact_name: str) -> None:
        record = self.find(contact_name)
        del self.data[record.id]

    def delete_by_id(self, record_id: str) -> None:
        if record_id not in self.data:
            raise KeyError("Record not found")
        del self.data[record_id]

    def get_upcoming_birthdays(self) -> list[dict]:
        upcoming_birthdays = []
        today = datetime.today().date()

        for record in self.data.values():
            if record.birthday is None:
                continue

            try:
                orig_birthday = datetime.strptime(record.birthday.value, DATE_FORMAT).date()
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
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime(DATE_FORMAT)
                })

        return upcoming_birthdays
