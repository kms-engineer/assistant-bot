import re
from typing import Dict


class NoteTextNormalizer:

    @staticmethod
    def normalize(entities: Dict) -> Dict:
        if 'note_text' not in entities or not entities['note_text']:
            return entities

        note_raw = entities['note_text'].strip()

        # Remove extra whitespace
        note_cleaned = re.sub(r'\s+', ' ', note_raw)

        # Remove surrounding quotes
        note_cleaned = note_cleaned.strip('\'"')

        entities['note_text'] = note_cleaned

        return entities
