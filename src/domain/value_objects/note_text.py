from dataclasses import dataclass
from ..validators.note_text_validator import NoteTextValidator
from .field import Field


@dataclass
class NoteText(Field):

    def __init__(self, value: str):
        NoteTextValidator.validate_and_raise(value)
        # Normalize: strip and remove extra whitespace
        normalized = " ".join(value.split())
        super().__init__(normalized)
