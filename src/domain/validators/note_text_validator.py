import re
from typing import Dict, Union


class NoteTextValidator:

    @staticmethod
    def validate(note_text: str) -> Union[str, bool]:
        if not isinstance(note_text, str):
            return "Note text must be a string"

        if not note_text or len(note_text.strip()) == 0:
            return "Note text cannot be empty or whitespace"

        # Note text should have some meaningful content
        trimmed = note_text.strip()
        if len(trimmed) < 1:
            return "Note text is too short"

        return True

    @staticmethod
    def validate_and_raise(note_text: str) -> None:
        result = NoteTextValidator.validate(note_text)
        if result is not True:
            raise ValueError(result)

    @staticmethod
    def normalize_for_nlp(entities: Dict) -> Dict:
        if 'note_text' not in entities or not entities['note_text']:
            return entities

        note_raw = entities['note_text'].strip()

        # Remove extra whitespace
        note_cleaned = re.sub(r'\s+', ' ', note_raw)

        # Remove surrounding quotes
        note_cleaned = note_cleaned.strip('\'"')

        entities['note_text'] = note_cleaned

        return entities
