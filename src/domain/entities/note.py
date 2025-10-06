import uuid
from typing import Optional
from ..value_objects.tag import Tag


class Note:

    def __init__(self, text: str, note_id: Optional[str] = None):
        if not text or not text.strip():
            raise ValueError("Note text cannot be empty")

        self.id = note_id if note_id else str(uuid.uuid4())
        self.text = text.strip()
        self.tags: list[Tag] = []

    def add_tag(self, tag: str) -> None:
        tag_obj = Tag(tag)
        if tag_obj in self.tags:
            raise ValueError("Tag already exists")
        self.tags.append(tag_obj)

    def remove_tag(self, tag: str) -> None:
        tag_obj = Tag(tag)
        if tag_obj not in self.tags:
            raise ValueError("Tag not found")
        self.tags.remove(tag_obj)

    def edit_text(self, new_text: str) -> None:
        if not new_text or not new_text.strip():
            raise ValueError("Note text cannot be empty")
        self.text = new_text.strip()

    def __str__(self) -> str:
        tags_str = ", ".join(str(tag) for tag in self.tags) if self.tags else "no tags"
        preview = self.text[:50] + "..." if len(self.text) > 50 else self.text
        return f"Note [{tags_str}]: {preview}"
