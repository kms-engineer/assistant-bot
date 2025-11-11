from typing import Optional

from fastmcp import FastMCP

from src.domain.value_objects import Email, Phone, Address, Name, Tag, Birthday
from src.infrastructure.storage.storage_factory import StorageFactory
from src.infrastructure.storage.storage_type import StorageType

from src.application.services.note_service import NoteService
from src.application.services.contact_service import ContactService


mcp = FastMCP("AssistantBot")

storage_type = StorageType.JSON
storage = StorageFactory.create_storage(storage_type)
contact_service = ContactService(storage)
note_service = NoteService(storage)


# Contact tools


@mcp.tool(
    title="Add contact",
    tags={"address book", "add contact"},
    description="Add a contact to address book with selected name and phone number",
)
def add_contact(name: str, phone: str):
    return contact_service.add_contact(Name(name), Phone(phone))


@mcp.tool(
    title="Remove contact",
    tags={"address book", "remove contact"},
    description="Remove a contact from the address book by name",
)
def remove_contact(name: str):
    return contact_service.delete_contact(name)


@mcp.tool(
    title="Edit contact email",
    tags={"address book", "edit contact", "email"},
    description="Set or replace the email for an existing contact",
)
def edit_contact(name: str, email: str):
    return contact_service.edit_email(name, Email(email))


@mcp.tool(
    title="Add email to contact",
    tags={"address book", "add email"},
    description="Add an email address to a contact",
)
def add_email(name: str, email: str):
    return contact_service.add_email(name, Email(email))


@mcp.tool(
    title="Remove contact email",
    tags={"address book", "remove email"},
    description="Remove the email address from a contact",
)
def remove_email(name: str):
    return contact_service.remove_email(name)


@mcp.tool(
    title="Edit contact address",
    tags={"address book", "edit address"},
    description="Set or replace the postal address for a contact",
)
def edit_address(name: str, address: str):
    return contact_service.edit_address(name, Address(address))


@mcp.tool(
    title="Add address to contact",
    tags={"address book", "add address"},
    description="Add a postal address to a contact",
)
def add_address(name: str, address: str):
    return contact_service.add_address(name, Address(address))


@mcp.tool(
    title="Remove contact address",
    tags={"address book", "remove address"},
    description="Remove the postal address from a contact",
)
def remove_address(name: str):
    return contact_service.remove_address(name)


@mcp.tool(
    title="Save address book",
    tags={"address book", "save"},
    description="Save the current address book to a file or storage",
)
def save_address_book(filename: Optional[str] = None):
    return contact_service.save_address_book(filename)


@mcp.tool(
    title="Load address book",
    tags={"address book", "load"},
    description="Load an address book from a file or storage",
)
def load_address_book(filename: Optional[str] = None, user_provided: bool = False):
    return contact_service.load_address_book(filename, user_provided=user_provided)


@mcp.tool(
    title="List contacts",
    tags={"address book", "list"},
    description="Return all contacts in the loaded address book",
)
def list_contacts():
    return contact_service.get_all_contacts()


@mcp.tool(
    title="Get contact birthday",
    tags={"address book", "birthday"},
    description="Get stored birthday for a contact (if any)",
)
def get_contact_birthday(name: str):
    return contact_service.get_birthday(name)


@mcp.tool(
    title="Add birthday to contact",
    tags={"address book", "birthday", "add"},
    description="Add a birthday for a contact (format depends on domain rules)",
)
def add_birthday(name: str, birthday: str):
    return contact_service.add_birthday(name, Birthday(birthday))


@mcp.tool(
    title="Get upcoming birthdays",
    tags={"address book", "birthday", "upcoming"},
    description="Return upcoming birthdays within given number of days",
)
def get_upcoming_birthdays(days_ahead: int):
    return contact_service.get_upcoming_birthdays(days_ahead)


@mcp.tool(
    title="Get contact phones",
    tags={"address book", "phones", "lookup"},
    description="Return phone numbers for a contact",
)
def get_contact_phone(name: str):
    return contact_service.get_phones(name)


@mcp.tool(
    title="Change contact phone",
    tags={"address book", "phones", "change"},
    description="Replace an existing phone number for a contact with a new one",
)
def change_phone(name: str, old_phone: str, new_phone: str):
    return contact_service.change_phone(name, Phone(old_phone), Phone(new_phone))


@mcp.tool(
    title="Search contacts",
    tags={"address book", "search"},
    description="Search contacts by text. Set exact=True for exact matching.",
)
def search_contacts(search_text: str, exact: bool = False):
    return contact_service.search(search_text, exact)


@mcp.tool(
    title="Get contacts current filename",
    tags={"address book", "metadata"},
    description="Get the filename currently used for the address book storage",
)
def get_contacts_current_filename():
    return contact_service.get_current_filename()


# Notes tools


@mcp.tool(
    title="Add numbers",
    tags={"math", "utility"},
    description="Add two integers and return the result",
)
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool(
    title="Add note",
    tags={"notes", "add"},
    description="Create a new note with title and text",
)
def add_note(title: str, text: str):
    return note_service.add_note(title, text)


@mcp.tool(
    title="Get note ids",
    tags={"notes", "ids"},
    description="Return set of currently loaded note ids",
)
def get_note_ids():
    return note_service.get_ids()


@mcp.tool(
    title="Delete note",
    tags={"notes", "delete"},
    description="Delete a note by id, title or tag. Set 'by' to 'id', 'title' or 'tag'.",
)
def remove_note(identifier: str, by: str = "id"):
    if by == "id":
        return note_service.delete_note_by_id(identifier)
    elif by == "title":
        return note_service.delete_note_by_title(identifier)
    elif by == "tag":
        return note_service.delete_note_by_tags(identifier)
    else:
        raise ValueError("'by' must be one of 'id', 'title', or 'tag'")


@mcp.tool(
    title="Delete note by id",
    tags={"notes", "delete", "id"},
    description="Delete a single note by its id",
)
def delete_note_by_id(note_id: str):
    return note_service.delete_note_by_id(note_id)


@mcp.tool(
    title="Delete note by title",
    tags={"notes", "delete", "title"},
    description="Delete notes that have the given title",
)
def delete_note_by_title(title: str):
    return note_service.delete_note_by_title(title)


@mcp.tool(
    title="Delete notes by tag",
    tags={"notes", "delete", "tag"},
    description="Delete all notes that contain the given tag",
)
def delete_notes_by_tag(tag: str):
    return note_service.delete_note_by_tags(tag)


@mcp.tool(
    title="Edit note",
    tags={"notes", "edit"},
    description="Edit the text of an existing note by id",
)
def edit_note(note_id: str, new_text: str):
    return note_service.edit_note(note_id, new_text)


@mcp.tool(
    title="Rename note",
    tags={"notes", "edit", "title"},
    description="Change the title of an existing note",
)
def rename_note(note_id: str, new_title: str):
    return note_service.rename_note(note_id, new_title)


@mcp.tool(
    title="Add tag to note",
    tags={"notes", "tags", "add"},
    description="Add a tag to a note (provide tag string)",
)
def add_tag(note_id: str, tag: str):
    return note_service.add_tag(note_id, Tag(tag))


@mcp.tool(
    title="Remove tag from note",
    tags={"notes", "tags", "remove"},
    description="Remove a tag from a note (provide tag string)",
)
def remove_tag(note_id: str, tag: str):
    return note_service.remove_tag(note_id, Tag(tag))


@mcp.tool(
    title="Get all notes", tags={"notes", "list"}, description="Return all loaded notes"
)
def get_all_notes():
    return note_service.get_all_notes()


@mcp.tool(
    title="Find note by title",
    tags={"notes", "lookup", "title"},
    description="Return the note that matches the given title (or None)",
)
def get_note_by_title(title: str):
    return note_service.get_note_id_by_title(title)


@mcp.tool(
    title="Search notes by content",
    tags={"notes", "search", "content"},
    description="Search notes by content substring (case-insensitive)",
)
def search_notes_by_content(query: str):
    return note_service.search_notes_by_content(query)


@mcp.tool(
    title="Search notes by title",
    tags={"notes", "search", "title"},
    description="Search notes by title (exact match)",
)
def search_notes_by_title(title: str):
    return note_service.search_notes_by_title(title)


@mcp.tool(
    title="Search notes by tag",
    tags={"notes", "search", "tag"},
    description="Search notes that contain a tag (case-insensitive)",
)
def search_notes_by_tag(tag: str):
    return note_service.search_notes_by_tag(tag)


@mcp.tool(
    title="List tags",
    tags={"notes", "tags", "list"},
    description="Return a mapping of tag -> count across all notes",
)
def list_tags():
    return note_service.list_tags()


@mcp.tool(
    title="Get notes grouped by tag",
    tags={"notes", "tags", "group"},
    description="Return notes grouped by their tags",
)
def get_notes_sorted_by_tag():
    return note_service.get_notes_sorted_by_tag()


@mcp.tool(
    title="Save notes",
    tags={"notes", "save"},
    description="Save notes to storage (optional filename)",
)
def save_notes(filename: Optional[str] = None):
    return note_service.save_notes(filename)


@mcp.tool(
    title="Load notes",
    tags={"notes", "load"},
    description="Load notes from storage (optional filename)",
)
def load_notes(filename: Optional[str] = None):
    return note_service.load_notes(filename)


@mcp.tool(
    title="Get notes current filename",
    tags={"notes", "metadata"},
    description="Get the filename currently used for notes storage",
)
def get_notes_current_filename():
    return note_service.get_current_filename()


if __name__ == "__main__":
    # Используем stdio транспорт для Claude Desktop
    mcp.run(transport="stdio")
