from typing import Any
from ...domain.entities.contact import Contact
from ...domain.entities.note import Note
from ...domain.value_objects.name import Name
from ...domain.value_objects.phone import Phone
from ...domain.value_objects.email import Email
from ...domain.value_objects.address import Address
from ...domain.value_objects.birthday import Birthday
from ...domain.value_objects.tag import Tag


class JsonSerializer:

    @staticmethod
    def contact_to_dict(contact: Contact) -> dict[str, Any]:
        return {
            "id": contact.id,
            "name": contact.name.value,
            "phones": [phone.value for phone in contact.phones],
            "birthday": contact.birthday.value if contact.birthday else None,
            "email": contact.email.value if contact.email else None,
            "address": contact.address.value if contact.address else None,
        }

    @staticmethod
    def dict_to_contact(data: dict[str, Any]) -> Contact:
        name_vo = Name(data["name"])
        contact = Contact(name_vo, contact_id=data["id"])

        for phone_str in data.get("phones", []):
            phone_vo = Phone(phone_str)
            contact.add_phone(phone_vo)

        if data.get("birthday"):
            birthday_vo = Birthday(data["birthday"])
            contact.add_birthday(birthday_vo)

        if data.get("email"):
            email_vo = Email(data["email"])
            contact.add_email(email_vo)

        if data.get("address"):
            address_vo = Address(data["address"])
            contact.add_address(address_vo)

        return contact

    @staticmethod
    def note_to_dict(note: Note) -> dict[str, Any]:
        return {
            "id": note.id,
            "text": note.text,
            "tags": [tag.value for tag in note.tags],
        }

    @staticmethod
    def dict_to_note(data: dict[str, Any]) -> Note:
        note = Note(data["text"], note_id=data["id"])

        for tag_str in data.get("tags", []):
            tag_vo = Tag(tag_str)
            note.add_tag(tag_vo)

        return note
