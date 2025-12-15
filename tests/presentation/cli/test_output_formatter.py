import pytest
from unittest.mock import MagicMock

from src.presentation.cli.output_formatter import (
    ContactFormatter,
    NoteFormatter,
    format_contacts_search,
    format_contacts_all,
    format_notes_search,
    format_notes_all,
)


def create_mock_contact(name, phones=None, email=None, birthday=None, address=None):
    contact = MagicMock()
    contact.name.value = name
    contact.phones = []
    if phones:
        for p in phones:
            phone_mock = MagicMock()
            phone_mock.value = p
            contact.phones.append(phone_mock)
    contact.email = None
    if email:
        contact.email = MagicMock()
        contact.email.value = email
    contact.birthday = birthday
    contact.address = None
    if address:
        contact.address = MagicMock()
        contact.address.value = address
    return contact


def create_mock_note(note_id, title, text, tags=None):
    note = MagicMock()
    note.id = note_id
    note.title = title
    note.text = text
    note.tags = []
    if tags:
        for t in tags:
            tag_mock = MagicMock()
            tag_mock.value = t
            note.tags.append(tag_mock)
    return note


class TestContactFormatter:

    def test_format_list_basic(self):
        contacts = [
            create_mock_contact("Alice", phones=["123-456"]),
            create_mock_contact("Bob", phones=["789-012"]),
        ]
        formatter = ContactFormatter()
        result = formatter.format_list(contacts)

        assert "Alice" in result
        assert "Bob" in result
        assert "123-456" in result

    def test_format_list_empty(self):
        formatter = ContactFormatter()
        result = formatter.format_list([])

        assert result == "No contacts found."

    def test_format_list_with_title(self):
        contacts = [create_mock_contact("Alice", phones=["123"])]
        formatter = ContactFormatter()
        result = formatter.format_list(contacts, title="Search results:")

        assert "Search results:" in result
        assert "Alice" in result

    def test_format_list_with_search_term(self):
        contacts = [create_mock_contact("Alice", phones=["123"])]
        formatter = ContactFormatter(search_term="Alice")
        result = formatter.format_list(contacts)

        assert "Alice" in result

    def test_format_list_compact(self):
        contacts = [
            create_mock_contact(
                "Alice",
                phones=["123"],
                email="alice@test.com",
                birthday="01.01.1990",
                address="123 Main St",
            )
        ]
        formatter_full = ContactFormatter(compact=False)
        formatter_compact = ContactFormatter(compact=True)

        result_full = formatter_full.format_list(contacts)
        result_compact = formatter_compact.format_list(contacts)

        assert "Birthday" in result_full
        assert "Address" in result_full
        assert "Birthday" not in result_compact

    def test_format_single(self):
        contact = create_mock_contact(
            "Alice",
            phones=["123", "456"],
            email="alice@test.com",
            address="Main St",
        )
        formatter = ContactFormatter()
        result = formatter.format_single(contact)

        assert "Name:" in result
        assert "Alice" in result
        assert "Phones:" in result
        assert "Email:" in result

    def test_format_single_with_highlight(self):
        contact = create_mock_contact("Alice", phones=["123"])
        formatter = ContactFormatter(search_term="Alice")
        result = formatter.format_single(contact)

        assert "Alice" in result


class TestNoteFormatter:

    def test_format_list_basic(self):
        notes = [
            create_mock_note("id-1", "Title 1", "Text content"),
            create_mock_note("id-2", "Title 2", "More text"),
        ]
        formatter = NoteFormatter()
        result = formatter.format_list(notes)

        assert "Title 1" in result
        assert "Title 2" in result

    def test_format_list_empty(self):
        formatter = NoteFormatter()
        result = formatter.format_list([])

        assert result == "No notes found."

    def test_format_list_with_title(self):
        notes = [create_mock_note("id-1", "Note", "Text")]
        formatter = NoteFormatter()
        result = formatter.format_list(notes, title="Found notes:")

        assert "Found notes:" in result

    def test_format_list_with_search_term(self):
        notes = [create_mock_note("id-1", "Important Note", "Text")]
        formatter = NoteFormatter(search_term="Important")
        result = formatter.format_list(notes)

        assert "Important" in result

    def test_format_list_with_tags(self):
        notes = [create_mock_note("id-1", "Note", "Text", tags=["work", "urgent"])]
        formatter = NoteFormatter()
        result = formatter.format_list(notes)

        assert "work" in result
        assert "urgent" in result

    def test_format_single(self):
        note = create_mock_note("id-123", "My Note", "Note content", tags=["tag1"])
        formatter = NoteFormatter()
        result = formatter.format_single(note)

        assert "ID:" in result
        assert "Title:" in result
        assert "Tags:" in result
        assert "Note content" in result

    def test_format_grouped_by_tag(self):
        notes = [create_mock_note("id-1", "Note 1", "Text")]
        formatter = NoteFormatter()
        result = formatter.format_grouped_by_tag({"work": notes})

        assert "work" in result

    def test_format_grouped_by_tag_empty(self):
        formatter = NoteFormatter()
        result = formatter.format_grouped_by_tag({})

        assert result == "No notes found."


class TestHelperFunctions:

    def test_format_contacts_search(self):
        contacts = [create_mock_contact("Alice", phones=["123"])]
        result = format_contacts_search(contacts, "Alice")

        assert "Found" in result
        assert "contact" in result.lower()
        assert "Alice" in result

    def test_format_contacts_all(self):
        contacts = [create_mock_contact("Alice", phones=["123"])]
        result = format_contacts_all(contacts)

        assert "All contacts" in result
        assert "Alice" in result

    def test_format_notes_search(self):
        notes = [create_mock_note("id-1", "Note", "Text")]
        result = format_notes_search(notes, "Note")

        assert "Found" in result
        assert "note" in result.lower()

    def test_format_notes_all(self):
        notes = [create_mock_note("id-1", "Note", "Text")]
        result = format_notes_all(notes)

        assert "All notes" in result


class TestEdgeCases:

    def test_contact_without_email(self):
        contact = create_mock_contact("Alice", phones=["123"])
        formatter = ContactFormatter()
        result = formatter.format_list([contact])

        assert "—" in result

    def test_contact_without_phones(self):
        contact = create_mock_contact("Alice")
        formatter = ContactFormatter()
        result = formatter.format_list([contact])

        assert "—" in result

    def test_note_long_text_truncated(self):
        long_text = "x" * 100
        note = create_mock_note("id-1", "Note", long_text)
        formatter = NoteFormatter()
        result = formatter.format_list([note])

        assert "..." in result

    def test_note_long_id_truncated(self):
        note = create_mock_note("a1b2c3d4-e5f6-7890-abcd-ef1234567890", "Note", "Text")
        formatter = NoteFormatter()
        result = formatter.format_list([note])

        assert "..." in result
