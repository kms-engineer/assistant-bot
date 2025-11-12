import os
from typing import List, Optional

from ..services.contact_service import ContactService
from ...domain.value_objects.address import Address
from ...domain.value_objects.birthday import Birthday
from ...domain.value_objects.email import Email
from ...domain.value_objects.name import Name
from ...domain.value_objects.phone import Phone
from ...presentation.cli.ui_messages import UIMessages
from ...domain.entities.contact import Contact
from ...presentation.cli.confirmation import confirm_action
from ...presentation.cli.selection import select_option, select_from_list


def _select_contact_by_name(service: ContactService, name: str) -> Optional[Contact]:
    matching_contacts = service.find_all_by_name(name)

    if not matching_contacts:
        raise KeyError(f"Contact '{name}' not found")

    if len(matching_contacts) == 1:
        return matching_contacts[0]

    # Multiple contacts found
    print(f"\nFound {len(matching_contacts)} contacts with name '{name}':")

    selected_idx = select_from_list(
        items=matching_contacts,
        prompt="Select contact:",
        formatter=str,
        allow_cancel=True,
    )

    if selected_idx is None:
        return None

    return matching_contacts[selected_idx]


def add_contact(args: List[str], service: ContactService) -> str:
    if len(args) < 2:
        raise ValueError("Add command requires 2 arguments: name and phone")

    name_vo = Name(args[0])
    phone_vo = Phone(args[1])

    # Check if contact with this name already exists
    existing_contacts = service.find_all_by_name(name_vo.value)

    if existing_contacts:
        # Show existing contacts and ask what to do
        print(f"\nContact(s) with name '{name_vo.value}' already exist:")
        for contact in existing_contacts:
            print(f"  - {contact}")

        options = [
            f"Add phone {phone_vo.value} to existing contact",
            f"Create new contact '{name_vo.value}' with phone {phone_vo.value}",
            "Cancel",
        ]

        choice = select_option(
            prompt="What would you like to do?",
            options=options,
            allow_cancel=False,  # We have cancel as option 3
        )

        if choice is None or choice == 2:  # Cancel
            return UIMessages.ACTION_CANCELLED
        elif choice == 0:  # Add phone to existing
            # If multiple contacts, pick the first one (or we could let user choose)
            contact = existing_contacts[0]
            return service.add_phone_to_contact(contact.id, phone_vo)
        else:  # choice == 1: Create new contact
            return service.create_new_contact(name_vo, phone_vo)

    # No existing contact, create new one
    return service.add_contact(name_vo, phone_vo)


def change_contact(args: List[str], service: ContactService) -> str:
    if len(args) < 3:
        raise ValueError(
            "Change command requires 3 arguments: name, old phone, and new phone"
        )

    name = args[0]
    old_phone_vo = Phone(args[1])
    new_phone_vo = Phone(args[2])

    contact = _select_contact_by_name(service, name)
    if not contact:
        return UIMessages.ACTION_CANCELLED

    # Ask for confirmation
    prompt = f"Change phone {old_phone_vo.value} to {new_phone_vo.value} for '{contact.name.value}'?"
    if not confirm_action(prompt, default=True):
        return UIMessages.ACTION_CANCELLED

    return service.edit_phone_by_id(contact.id, old_phone_vo, new_phone_vo)


def remove_phone(args: List[str], service: ContactService) -> str:
    if len(args) < 2:
        raise ValueError("remove-phone command requires 2 arguments: name and phone")

    name = args[0]
    phone_vo = Phone(args[1])

    contact = _select_contact_by_name(service, name)
    if not contact:
        return UIMessages.ACTION_CANCELLED

    # Ask for confirmation
    prompt = f"Remove phone {phone_vo.value} from '{contact.name.value}'?"
    if not confirm_action(prompt, default=False):
        return UIMessages.ACTION_CANCELLED

    return service.remove_phone_by_id(contact.id, phone_vo)


def delete_contact(args: List[str], service: ContactService) -> str:
    if len(args) < 1:
        raise ValueError("delete-contact command requires 1 argument: name")

    name = args[0]

    # Find all contacts with this name
    matching_contacts = service.find_all_by_name(name)

    if not matching_contacts:
        raise KeyError(f"Contact '{name}' not found")

    contact_to_delete = None

    if len(matching_contacts) > 1:
        # Multiple contacts found, ask user to select
        print(f"\nFound {len(matching_contacts)} contacts with name '{name}':")

        from ...presentation.cli.selection import select_from_list

        selected_idx = select_from_list(
            items=matching_contacts,
            prompt="Select contact to delete:",
            formatter=str,
            allow_cancel=True,
        )

        if selected_idx is None:
            return UIMessages.ACTION_CANCELLED

        contact_to_delete = matching_contacts[selected_idx]
    else:
        contact_to_delete = matching_contacts[0]

    # Ask for confirmation
    prompt = UIMessages.CONFIRM_DELETE_CONTACT.format(name=str(contact_to_delete))
    if not confirm_action(prompt, default=False):
        return UIMessages.ACTION_CANCELLED

    return service.delete_contact_by_id(contact_to_delete.id)


def show_phone(args: List[str], service: ContactService) -> str:
    if len(args) < 1:
        raise ValueError("show-phone command requires 1 argument: name")

    name = args[0]

    contact = _select_contact_by_name(service, name)
    if not contact:
        return UIMessages.ACTION_CANCELLED

    if not contact.phones:
        return f"{contact.name.value} has no phone numbers."

    phones_str = "; ".join([phone.value for phone in contact.phones])
    return f"{contact.name.value}: {phones_str}"


def show_all(service: ContactService) -> str:
    contacts = service.get_all_contacts()

    if not contacts:
        return "No contacts found."

    lines = ["All contacts:"]
    for contact in contacts:
        lines.append(str(contact))
    return "\n".join(lines)


def add_birthday(args: List[str], service: ContactService) -> str:
    if len(args) < 2:
        raise ValueError(
            "Add-birthday command requires 2 arguments: name and birthday (DD.MM.YYYY)"
        )

    name = args[0]
    birthday_vo = Birthday(args[1])

    contact = _select_contact_by_name(service, name)
    if not contact:
        return UIMessages.ACTION_CANCELLED

    return service.add_birthday_by_id(contact.id, birthday_vo)


def show_birthday(args: List[str], service: ContactService) -> str:
    if len(args) < 1:
        raise ValueError("Show-birthday command requires 1 argument: name")

    name = args[0]

    contact = _select_contact_by_name(service, name)
    if not contact:
        return UIMessages.ACTION_CANCELLED

    if contact.birthday:
        return f"{contact.name.value}'s birthday: {contact.birthday.value}"
    else:
        return f"No birthday set for {contact.name.value}."


def remove_birthday(args: List[str], service: ContactService) -> str:
    if len(args) < 1:
        raise ValueError("Remove-birthday command requires 1 argument: name")

    name = args[0]

    contact = _select_contact_by_name(service, name)
    if not contact:
        return UIMessages.ACTION_CANCELLED

    if not contact.birthday:
        return f"{contact.name.value} has no birthday set."

    if not confirm_action(
        f"Remove birthday {contact.birthday.value} from {contact.name.value}?"
    ):
        return UIMessages.ACTION_CANCELLED

    return service.remove_birthday_by_id(contact.id)


def birthdays(args: List[str], service: ContactService) -> str:
    if len(args) < 1:
        days = 7
    else:
        try:
            days = int(args[0])
        except ValueError:
            raise ValueError(f"Invalid amount of days ahead: {args[0]}")
    if days > 365:
        raise ValueError(f"Max amount of days for upcoming birthdays is 365.")

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

    name = args[0]
    email_vo = Email(args[1])

    contact = _select_contact_by_name(service, name)
    if not contact:
        return UIMessages.ACTION_CANCELLED

    return service.add_email_by_id(contact.id, email_vo)


def edit_email(args: List[str], service: ContactService) -> str:
    if len(args) < 2:
        raise ValueError(
            "Edit-email command requires 2 arguments: name and new email address"
        )

    name = args[0]
    email_vo = Email(args[1])

    contact = _select_contact_by_name(service, name)
    if not contact:
        return UIMessages.ACTION_CANCELLED

    return service.edit_email_by_id(contact.id, email_vo)


def remove_email(args: List[str], service: ContactService):
    if len(args) < 1:
        raise ValueError("Remove-email command requires 1 argument: name")

    name = args[0]

    contact = _select_contact_by_name(service, name)
    if not contact:
        return UIMessages.ACTION_CANCELLED

    # Ask for confirmation
    prompt = UIMessages.CONFIRM_REMOVE_EMAIL.format(name=contact.name.value)
    if not confirm_action(prompt, default=False):
        return UIMessages.ACTION_CANCELLED

    return service.remove_email_by_id(contact.id)


def add_address(args: List[str], service: ContactService) -> str:
    if len(args) < 2:
        raise ValueError("Add-address command requires 2 arguments: name and address")

    name = args[0]
    address_vo = Address(" ".join(args[1:]))

    contact = _select_contact_by_name(service, name)
    if not contact:
        return UIMessages.ACTION_CANCELLED

    return service.add_address_by_id(contact.id, address_vo)


def edit_address(args: List[str], service: ContactService) -> str:
    if len(args) < 2:
        raise ValueError(
            "Edit-address command requires 2 arguments: name and new address"
        )

    name = args[0]
    address_vo = Address(" ".join(args[1:]))

    contact = _select_contact_by_name(service, name)
    if not contact:
        return UIMessages.ACTION_CANCELLED

    return service.edit_address_by_id(contact.id, address_vo)


def remove_address(args: List[str], service: ContactService):
    if len(args) < 1:
        raise ValueError("Remove-address command requires 1 argument: name")

    name = args[0]

    contact = _select_contact_by_name(service, name)
    if not contact:
        return UIMessages.ACTION_CANCELLED

    # Ask for confirmation
    prompt = UIMessages.CONFIRM_REMOVE_ADDRESS.format(name=contact.name.value)
    if not confirm_action(prompt, default=False):
        return UIMessages.ACTION_CANCELLED

    return service.remove_address_by_id(contact.id)


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

    # Ask for confirmation (loading overwrites current data)
    if not confirm_action(UIMessages.CONFIRM_LOAD_FILE, default=False):
        return UIMessages.ACTION_CANCELLED

    count = service.load_address_book(filename, user_provided=True)
    return f"Address book loaded from {service.get_current_filename()}. {count} contact(s) found."


def hello() -> str:
    return "How can I help you?"


def help(nlp_mode: bool = False) -> str:
    return UIMessages.get_command_list(nlp_mode)


def clear() -> str:
    os.system("clear" if os.name == "posix" else "cls")
    return ""
