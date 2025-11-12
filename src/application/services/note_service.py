from collections import defaultdict
from typing import Optional, Set, Any

from ...domain.entities.note import Note
from ...domain.utils.id_generator import IDGenerator
from ...domain.value_objects.tag import Tag
from ...infrastructure.persistence.data_path_resolver import (
    DEFAULT_NOTES_FILE,
    DEFAULT_ADDRESS_BOOK_DATABASE_NAME,
)
from ...infrastructure.persistence.domain_storage_adapter import DomainStorageAdapter
from ...infrastructure.serialization.json_serializer import JsonSerializer
from ...infrastructure.storage.json_storage import JsonStorage
from ...infrastructure.storage.storage import Storage
from ...infrastructure.storage.storage_type import StorageType


class NoteService:

    def __init__(self, storage: Optional[Storage] = None, serializer: Optional[JsonSerializer] = None):
        raw_storage = storage if storage else JsonStorage()
        self.storage = DomainStorageAdapter(raw_storage, serializer)
        self.notes : dict[Any, Any] = {}
        self.raw_storage = raw_storage
        if raw_storage.storage_type == StorageType.SQLITE:
            self._current_filename = DEFAULT_ADDRESS_BOOK_DATABASE_NAME
            self._default_filename = DEFAULT_ADDRESS_BOOK_DATABASE_NAME
        else:
            self._current_filename = DEFAULT_NOTES_FILE
            self._default_filename = DEFAULT_NOTES_FILE

    def get_ids(self) -> Set[str]:
        return set(self.notes.keys())

    def get_titles(self) -> Set[str]:
        return set([item for item in self.notes.values()])

    def load_notes(self, filename: str | None = None) -> int:
        # Use the appropriate default based on storage type
        if filename is None:
            filename = self._default_filename
        loaded_notes, normalized_filename = self.storage.load_notes(
            filename, default=[]
        )

        self.notes = loaded_notes
        # For SQLite, keep the original database filename
        if self.raw_storage.storage_type == StorageType.SQLITE:
            self._current_filename = self._default_filename
        else:
            self._current_filename = normalized_filename

        return len(self.notes)

    def save_notes(self, filename: Optional[str] = None) -> str:
        target = filename if filename else self._current_filename

        saved_filename = self.storage.save_notes(self.notes, target)
        self._current_filename = saved_filename
        return saved_filename

    def add_note(self, title: str, text: str) -> str:
        note = Note.create(
            title, text, lambda: IDGenerator.generate_unique_id(lambda: self.get_ids())
        )
        self.notes[note.id] = note
        return note.id

    def edit_note(self, note_id: str, new_text: str) -> str:
        if note_id not in self.notes:
            raise KeyError("Note not found")
        self.notes[note_id].edit_text(new_text)
        return "Note updated."

    def rename_note(self, note_id: str, new_title: str) -> str:
        if note_id not in self.notes:
            raise KeyError("Note not found")
        self.notes[note_id].edit_title(new_title)
        return "Note title updated."

    def delete_note_by_id(self, note_id: str) -> str:
        if note_id not in self.notes:
            raise KeyError("Note not found")
        del self.notes[note_id]
        return "Note deleted."

    def delete_note_by_title(self, title: str) -> str:
        if not title or not title.strip():
            raise KeyError("Note title can't be empty")
        found_notes = list(note for note in self.notes.values() if note.title == title)
        for note in found_notes:
            self.delete_note_by_id(note.id)
        return "Note(s) deleted"

    def delete_note_by_tags(self, tag: str) -> str:
        if not tag or not tag.strip():
            raise KeyError("Note title can't be empty")
        search_tag = Tag(tag)
        found_notes = list(
            note for note in self.notes.values() if search_tag in note.tags
        )
        for note in found_notes:
            self.delete_note_by_id(note.id)
        return "Note(s) deleted"

    def add_tag(self, note_id: str, tag: Tag) -> str:
        if note_id not in self.notes:
            raise KeyError("Note not found")
        self.notes[note_id].add_tag(tag)
        return "Tag added."

    def remove_tag(self, note_id: str, tag: Tag) -> str:
        if note_id not in self.notes:
            raise KeyError("Note not found")
        self.notes[note_id].remove_tag(tag)
        return "Tag removed."

    def get_all_notes(self) -> list[Note]:
        return list(self.notes.values())

    def get_note_by_id(self, note_id: str) -> Optional[Note]:
        return self.notes.get(note_id)

    def search_notes(self, query: str) -> list[Note]:
        query_lower = query.lower()
        return [
            note for note in self.notes.values() if query_lower in note.text.lower()
        ]

    def get_note_id_by_title(self, title: str):
        if not title or not title.strip():
            raise KeyError("Note title can't be empty")
        title = title.strip()
        return next((note for note in self.notes.values() if note.title == title), None)

    def search_notes_by_content(self, query: str) -> list[Note]:
        query_lower = query.lower()
        return [
            note for note in self.notes.values() if query_lower in note.text.lower()
        ]

    def search_notes_by_title(self, query: str) -> list[Note]:
        if not query or not query.strip():
            raise KeyError("Note title can't be empty")
        return list(note for note in self.notes.values() if query in note.title.lower())

    def search_notes_by_tag(self, tag: str) -> list[Note]:
        tag_lower = tag.lower()
        return [
            note
            for note in self.notes.values()
            if any(tag_lower == t.value.lower() for t in note.tags)
        ]

    def search_by_tag(self, tag: str) -> list[Note]:
        return self.search_notes_by_tag(tag)

    def list_tags(self) -> dict[str, int]:
        tag_counts : dict[str, int] = {}
        for note in self.notes.values():
            for tag in note.tags:
                tag_value = tag.value
                tag_counts[tag_value] = tag_counts.get(tag_value, 0) + 1
        return dict(sorted(tag_counts.items()))

    def get_notes_sorted_by_title(self) -> dict[str, list[Note]]:
        groups: defaultdict[str, list[Note]] = defaultdict(list)
        for note in self.notes.values():
            title = note.title or ""
            groups[title].append(note)
        return dict(sorted(groups.items(), key=lambda item: item[0].lower()))

    def get_notes_sorted_by_tag(self) -> dict[str, list[Note]]:
        tag_groups: dict[str, list[Note]] = {}
        for note in self.notes.values():
            if not note.tags:
                if "untagged" not in tag_groups:
                    tag_groups["untagged"] = []
                tag_groups["untagged"].append(note)
            else:
                for tag in note.tags:
                    tag_value = tag.value
                    if tag_value not in tag_groups:
                        tag_groups[tag_value] = []
                    tag_groups[tag_value].append(note)

        return dict(sorted(tag_groups.items()))

    def get_current_filename(self) -> str:
        return self._current_filename
