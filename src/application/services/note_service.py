from typing import Optional, Set
from ...domain.entities.note import Note
from ...domain.utils.id_generator import IDGenerator
from ...infrastructure.storage.storage_interface import StorageInterface
from ...infrastructure.storage.json_storage import JsonStorage
from ...infrastructure.serialization.json_serializer import JsonSerializer
from ...infrastructure.persistence.data_path_resolver import DEFAULT_NOTES_FILE
from ...infrastructure.persistence.domain_storage_adapter import DomainStorageAdapter


class NoteService:

    def __init__(self, storage: StorageInterface = None, serializer: JsonSerializer = None):
        raw_storage = storage if storage else JsonStorage()
        self.storage = DomainStorageAdapter(raw_storage, serializer)
        self.notes: dict[str, Note] = {}
        self._current_filename = DEFAULT_NOTES_FILE

    def get_ids(self) -> Set[str]:
        return set(self.notes.keys())

    def load_notes(self, filename: str = DEFAULT_NOTES_FILE) -> int:
        loaded_notes, normalized_filename = self.storage.load_notes(
            filename,
            default=[]
        )

        self.notes = loaded_notes
        self._current_filename = normalized_filename

        return len(self.notes)

    def save_notes(self, filename: Optional[str] = None) -> str:
        target = filename if filename else self._current_filename

        saved_filename = self.storage.save_notes(
            self.notes,
            target
        )
        self._current_filename = saved_filename
        return saved_filename

    def add_note(self, text: str) -> str:
        note = Note.create(
            text,
            lambda: IDGenerator.generate_unique_id(
                lambda: self.get_ids()
            )
        )
        self.notes[note.id] = note
        return note.id

    def edit_note(self, note_id: str, new_text: str) -> str:
        if note_id not in self.notes:
            raise KeyError("Note not found")
        self.notes[note_id].edit_text(new_text)
        return "Note updated."

    def delete_note(self, note_id: str) -> str:
        if note_id not in self.notes:
            raise KeyError("Note not found")
        del self.notes[note_id]
        return "Note deleted."

    def add_tag(self, note_id: str, tag: str) -> str:
        if note_id not in self.notes:
            raise KeyError("Note not found")
        self.notes[note_id].add_tag(tag)
        return "Tag added."

    def remove_tag(self, note_id: str, tag: str) -> str:
        if note_id not in self.notes:
            raise KeyError("Note not found")
        self.notes[note_id].remove_tag(tag)
        return "Tag removed."

    def get_all_notes(self) -> list[Note]:
        return list(self.notes.values())

    def search_notes(self, query: str) -> list[Note]:
        query_lower = query.lower()
        return [note for note in self.notes.values() if query_lower in note.text.lower()]

    def search_by_tag(self, tag: str) -> list[Note]:
        tag_lower = tag.lower()
        return [
            note for note in self.notes.values()
            if any(tag_lower == t.value.lower() for t in note.tags)
        ]

    def get_current_filename(self) -> str:
        return self._current_filename
