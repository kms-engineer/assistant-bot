from typing import Union
from src.config import ValidationConfig
from src.domain.validators.base_validator import BaseValidator


class NoteTextValidator(BaseValidator):

    @staticmethod
    def validate(note_text: str) -> Union[str, bool]:
        if not isinstance(note_text, str):
            return ValidationConfig.NOTE_ERROR_NOT_STRING

        if not note_text or len(note_text.strip()) == 0:
            return ValidationConfig.NOTE_ERROR_EMPTY

        trimmed = note_text.strip()
        if len(trimmed) < 1:
            return ValidationConfig.NOTE_ERROR_TOO_SHORT

        return True
