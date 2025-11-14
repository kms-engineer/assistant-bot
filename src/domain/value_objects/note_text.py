from dataclasses import dataclass
from src.domain.validators.note_text_validator import NoteTextValidator
from src.domain.value_objects.field import Field


@dataclass
class NoteText(Field):

    def __init__(self, value: str):
        NoteTextValidator.validate_and_raise(value)
        # Normalize: strip and remove extra whitespace
        normalized = " ".join(value.split())
        super().__init__(normalized)
