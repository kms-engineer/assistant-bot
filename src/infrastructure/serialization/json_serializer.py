from typing import Any
from ...domain.entities.contact import Contact
from ...domain.entities.note import Note


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
        contact = Contact(data["name"], contact_id=data["id"])

        for phone in data.get("phones", []):
            contact.add_phone(phone)

        if data.get("birthday"):
            contact.add_birthday(data["birthday"])

        if data.get("email"):
            contact.add_email(data["email"])

        if data.get("address"):
            contact.add_address(data["address"])

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

        for tag in data.get("tags", []):
            note.add_tag(tag)

        return note
