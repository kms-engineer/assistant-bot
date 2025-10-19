from typing import List

from ..services.contact_service import ContactService
from ...presentation.cli.ui_messages import UIMessages


def add_contact(args: List[str], service: ContactService) -> str:
    if len(args) < 2:
        raise ValueError("Add command requires 2 arguments: name and phone")

    name, phone = args[0], args[1]
    return service.add_contact(name, phone)


def change_contact(args: List[str], service: ContactService) -> str:
    if len(args) < 3:
        raise ValueError("Change command requires 3 arguments: name, old phone, and new phone")

    name, old_phone, new_phone = args[0], args[1], args[2]
    return service.change_phone(name, old_phone, new_phone)


def delete_contact(args: List[str], service: ContactService) -> str:
    if len(args) < 1:
        raise ValueError("Delete-contact command requires 1 argument: name")

    name = args[0]
    return service.delete_contact(name)


def show_phone(args: List[str], service: ContactService) -> str:
    if len(args) < 1:
        raise ValueError("Phone command requires 1 argument: name")

    name = args[0]
    phones = service.get_phones(name)

    if not phones:
        return f"{name} has no phone numbers."

    phones_str = "; ".join(phones)
    return f"{name}: {phones_str}"


def show_all(args: List[str], service: ContactService) -> str:
    contacts = service.get_all_contacts()

    if not contacts:
        return "No contacts found."

    lines = ["All contacts:"]
    for contact in contacts:
        lines.append(str(contact))
    return "\n".join(lines)


def add_birthday(args: List[str], service: ContactService) -> str:
    if len(args) < 2:
        raise ValueError("Add-birthday command requires 2 arguments: name and birthday (DD.MM.YYYY)")

    name, birthday = args[0], args[1]
    return service.add_birthday(name, birthday)


def show_birthday(args: List[str], service: ContactService) -> str:
    if len(args) < 1:
        raise ValueError("Show-birthday command requires 1 argument: name")

    name = args[0]
    birthday = service.get_birthday(name)

    if birthday:
        return f"{name}'s birthday: {birthday}"
    else:
        return f"No birthday set for {name}."


def birthdays(args: List[str], service: ContactService) -> str:
    if len(args) < 1:
        days = 7
    else:
        try:
            days = int(args[0])
            if days > 365:
                return f"Max amount of days for upcoming birthdays is 365."
        except ValueError:
            raise ValueError(f"Invalid amount of days ahead: {args[0]}")

    upcoming = service.get_upcoming_birthdays(days)

    if not upcoming:
        return f"No upcoming birthdays in the next {days} days."

    lines = ["Upcoming birthdays:"]
    for contact in upcoming:
        lines.append(f"{contact['name']}: {contact['birthdays_date']}")
    return "\n".join(lines)


def add_email(args: List[str], service: ContactService) -> str:
    if len(args) < 2:
        raise ValueError("Add-email command requires 2 arguments: name and email")

    name, email = args[0], args[1]
    return service.add_email(name, email)


def edit_email(args: List[str], service: ContactService) -> str:
    if len(args) < 2:
        raise ValueError("Edit-email command requires 2 arguments: name and new email adress")

    name, email = args[0], args[1]
    return service.edit_email(name, email)


def remove_email(args: List[str], service: ContactService):
    if len(args) < 1:
        raise ValueError("Remove-email command requires 1 argument: name")

    name = args[0]
    return service.remove_email(name)


def add_address(args: List[str], service: ContactService) -> str:
    if len(args) < 2:
        raise ValueError("Add-address command requires 2 arguments: name and address")

    name = args[0]
    address = " ".join(args[1:])
    return service.add_address(name, address)


def edit_address(args: List[str], service: ContactService) -> str:
    if len(args) < 2:
        raise ValueError("Edit-address command requires 2 arguments: name and new adress")

    name, address = args[0], " ".join(args[1:])
    return service.edit_address(name, address)


def remove_address(args: List[str], service: ContactService):
    if len(args) < 1:
        raise ValueError("Remove-address command requires 1 argument: name")

    name = args[0]
    return service.remove_address(name)


def search(args: List[str], service: ContactService) -> str:
    if not args:
        raise ValueError("Search command requires a search_text argument")

    search_text = args[0]
    contacts = service.search(search_text)

    if not contacts:
        return f"No contact name, email or phone found for provided search text: {search_text}"

    lines = ["Found contacts:"]
    for contact in contacts:
        lines.append(str(contact))
    return "\n".join(lines)


def find(args: List[str], service: ContactService) -> str:
    if not args:
        raise ValueError("Find command requires a search_text argument")

    search_text = args[0]
    contacts = service.search(search_text, exact=True)

    if not contacts:
        return f"No contact name, email or phone found for provided search text: {search_text}"

    lines = ["Found contacts:"]
    for contact in contacts:
        lines.append(str(contact))
    return "\n".join(lines)


def save_contacts(args: List[str], service: ContactService) -> str:
    if not args:
        raise ValueError("Save command requires a filename argument")

    filename = args[0]
    saved_filename = service.save_address_book(filename, user_provided=True)
    return f"Address book saved to {saved_filename}."


def load_contacts(args: List[str], service: ContactService) -> str:
    if not args:
        raise ValueError("Load command requires a filename argument")

    filename = args[0]
    count = service.load_address_book(filename, user_provided=True)
    return f"Address book loaded from {service.get_current_filename()}. {count} contact(s) found."


def hello(args: List[str], service: ContactService) -> str:
    return "How can I help you?"

