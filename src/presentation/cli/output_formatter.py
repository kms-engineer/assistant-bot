from typing import List, Optional, TYPE_CHECKING

from src.presentation.cli.table_formatter import TableFormatter
from src.presentation.cli.search_highlighter import SearchHighlighter

if TYPE_CHECKING:
    from src.domain.entities.contact import Contact
    from src.domain.entities.note import Note


class ContactFormatter:
    HEADERS = ["Name", "Phones", "Email", "Birthday", "Address"]
    HEADERS_COMPACT = ["Name", "Phones", "Email"]

    def __init__(self, search_term: Optional[str] = None, compact: bool = False):
        self._highlighter = SearchHighlighter()
        self._compact = compact
        if search_term:
            self._highlighter.set_search_term(search_term)

    def format_list(self, contacts: List["Contact"], title: str = "") -> str:
        if not contacts:
            return "No contacts found."

        rows = [self._contact_to_row(c) for c in contacts]
        headers = self.HEADERS_COMPACT if self._compact else self.HEADERS

        formatter = TableFormatter(
            headers=headers,
            max_col_width=40,
        )

        col_highlighter = self._highlighter.create_column_highlighter(None)
        table = formatter.format(rows, highlighter=col_highlighter)

        if title:
            return f"{title}\n{table}"
        return table

    def _contact_to_row(self, contact: "Contact") -> List[str]:
        phones = "; ".join(p.value for p in contact.phones) if contact.phones else "—"
        email = contact.email.value if contact.email else "—"

        if self._compact:
            return [contact.name.value, phones, email]

        birthday = str(contact.birthday) if contact.birthday else "—"
        address = contact.address.value if contact.address else "—"

        return [contact.name.value, phones, email, birthday, address]

    def format_single(self, contact: "Contact") -> str:
        lines = []
        lines.append(f"Name:     {self._highlight(contact.name.value)}")

        phones = "; ".join(p.value for p in contact.phones) if contact.phones else "—"
        lines.append(f"Phones:   {self._highlight(phones)}")

        email = contact.email.value if contact.email else "—"
        lines.append(f"Email:    {self._highlight(email)}")

        if contact.birthday:
            lines.append(f"Birthday: {contact.birthday}")

        if contact.address:
            lines.append(f"Address:  {self._highlight(contact.address.value)}")

        return "\n".join(lines)

    def _highlight(self, text: str) -> str:
        return self._highlighter.highlight(text)


class NoteFormatter:
    HEADERS = ["ID", "Title", "Tags", "Text Preview"]
    HEADERS_SIMPLE = ["ID", "Title", "Tags"]

    def __init__(self, search_term: Optional[str] = None, show_preview: bool = True):
        self._highlighter = SearchHighlighter()
        self._show_preview = show_preview
        if search_term:
            self._highlighter.set_search_term(search_term)

    def format_list(self, notes: List["Note"], title: str = "") -> str:
        if not notes:
            return "No notes found."

        rows = [self._note_to_row(n) for n in notes]
        headers = self.HEADERS if self._show_preview else self.HEADERS_SIMPLE

        formatter = TableFormatter(
            headers=headers,
            max_col_width=35,
        )

        col_highlighter = self._highlighter.create_column_highlighter(None)
        table = formatter.format(rows, highlighter=col_highlighter)

        if title:
            return f"{title}\n{table}"
        return table

    def _note_to_row(self, note: "Note") -> List[str]:
        short_id = note.id[:8] + "..." if len(note.id) > 11 else note.id
        tags = ", ".join(t.value for t in note.tags) if note.tags else "—"
        title = note.title if note.title else "—"

        if self._show_preview:
            text_preview = note.text[:50] + "..." if len(note.text) > 50 else note.text
            return [short_id, title, tags, text_preview]

        return [short_id, title, tags]

    def format_single(self, note: "Note") -> str:
        lines = []
        lines.append(f"ID:    {note.id}")

        if note.title:
            lines.append(f"Title: {self._highlight(note.title)}")

        if note.tags:
            tags_str = ", ".join(t.value for t in note.tags)
            lines.append(f"Tags:  {tags_str}")

        lines.append(f"\n{self._highlight(note.text)}")

        return "\n".join(lines)

    def _highlight(self, text: str) -> str:
        return self._highlighter.highlight(text)

    def format_grouped_by_tag(self, notes_by_tag: dict) -> str:
        if not notes_by_tag:
            return "No notes found."

        lines = []
        for tag, notes in sorted(notes_by_tag.items()):
            lines.append(f"\n{'='*50}")
            lines.append(f"Tag: {tag} ({len(notes)} notes)")
            lines.append("="*50)

            formatter = NoteFormatter(show_preview=True)
            lines.append(formatter.format_list(notes))

        return "\n".join(lines)


def format_contacts_search(
    contacts: List["Contact"],
    search_term: str,
) -> str:
    formatter = ContactFormatter(search_term=search_term)
    return formatter.format_list(contacts, title=f"Found {len(contacts)} contact(s):")


def format_contacts_all(contacts: List["Contact"]) -> str:
    formatter = ContactFormatter(compact=False)
    return formatter.format_list(contacts, title=f"All contacts ({len(contacts)}):")


def format_notes_search(
    notes: List["Note"],
    search_term: str,
) -> str:
    formatter = NoteFormatter(search_term=search_term)
    return formatter.format_list(notes, title=f"Found {len(notes)} note(s) matching '{search_term}':")


def format_notes_all(notes: List["Note"]) -> str:
    formatter = NoteFormatter(show_preview=True)
    return formatter.format_list(notes, title=f"All notes ({len(notes)}):")
