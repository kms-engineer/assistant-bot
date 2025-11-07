from typing import Callable

from .entity import Entity
from ..value_objects.tag import Tag


class Note(Entity):

    def __init__(self, title: str, text: str, note_id: str):
        if not title or not title.strip():
            raise ValueError("Note title cannot be empty")
        if not text or not text.strip():
            raise ValueError("Note text cannot be empty")
        if not note_id:
            raise ValueError("Note ID is required")

        self.id = note_id
        self.title = title
        self.text = text.strip()
        self.tags: list[Tag] = []

    @classmethod
    def create(cls, title: str, text: str, id_generator: Callable[[], str]) -> 'Note':
        note_id = id_generator()
        return cls(title, text, note_id)

    def add_tag(self, tag: Tag) -> None:
        if tag in self.tags:
            raise ValueError("Tag already exists")
        self.tags.append(tag)

    def remove_tag(self, tag: Tag) -> None:
        if tag not in self.tags:
            raise ValueError("Tag not found")
        self.tags.remove(tag)

    def edit_title(self, new_title: str) -> None:
        if not new_title or not new_title.strip():
            raise ValueError("New title cannot be empty")
        self.title = new_title.strip()

    def edit_text(self, new_text: str) -> None:
        if not new_text or not new_text.strip():
            raise ValueError("Note text cannot be empty")
        self.text = new_text.strip()

    def __str__(self) -> str:
        tags_str = ", ".join(str(tag) for tag in self.tags) if self.tags else "no tags"
        preview = self.text[:50] + "..." if len(self.text) > 50 else self.text
        return f"Note '{self.title}'\n[{tags_str}]:\n{preview}"
