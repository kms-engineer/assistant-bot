import uuid
from typing import Optional

from .entity import Entity
from typing import Callable
from ..value_objects.tag import Tag


class Note(Entity):

    def __init__(self, text: str, note_id: str):
        if not text or not text.strip():
            raise ValueError("Note text cannot be empty")
        if not note_id:
            raise ValueError("Note ID is required")

        self.id = note_id
        self.text = text.strip()
        self.tags: list[Tag] = []

    @classmethod
    def create(cls, text: str, id_generator: Callable[[], str]) -> 'Note':
        note_id = id_generator()
        return cls(text, note_id)

    def add_tag(self, tag: Tag) -> None:
        if tag in self.tags:
            raise ValueError("Tag already exists")
        self.tags.append(tag)

    def remove_tag(self, tag: Tag) -> None:
        if tag not in self.tags:
            raise ValueError("Tag not found")
        self.tags.remove(tag)

    def edit_text(self, new_text: str) -> None:
        if not new_text or not new_text.strip():
            raise ValueError("Note text cannot be empty")
        self.text = new_text.strip()

    def __str__(self) -> str:
        tags_str = ", ".join(str(tag) for tag in self.tags) if self.tags else "no tags"
        preview = self.text[:50] + "..." if len(self.text) > 50 else self.text
        return f"Note [{tags_str}]: {preview}"
