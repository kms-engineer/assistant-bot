import re
from typing import Dict
from .base import EntityValidator


class NameValidator(EntityValidator):

    def validate(self, entities: Dict) -> Dict:
        if 'name' not in entities or not entities['name']:
            return entities

        name_raw = entities['name'].strip()

        # Capitalize each word
        name_cleaned = ' '.join(word.capitalize() for word in name_raw.split())

        # Remove extra whitespace
        name_cleaned = re.sub(r'\s+', ' ', name_cleaned)

        entities['name'] = name_cleaned

        # Validate: should have at least 2 characters
        if len(name_cleaned) < 2:
            entities['_name_valid'] = False
            self._add_error(entities, f"Name too short: {name_cleaned}")
        else:
            entities['_name_valid'] = True

        return entities


class TagValidator(EntityValidator):

    def validate(self, entities: Dict) -> Dict:
        if 'tag' not in entities or not entities['tag']:
            return entities

        tag_raw = entities['tag'].strip()

        if not tag_raw.startswith('#'):
            tag_raw = '#' + tag_raw

        tag_raw = re.sub(r'[^\w#]', '', tag_raw)

        entities['tag'] = tag_raw
        return entities


class NoteValidator(EntityValidator):

    def validate(self, entities: Dict) -> Dict:
        if 'note_text' not in entities or not entities['note_text']:
            return entities

        note_raw = entities['note_text'].strip()

        note_cleaned = re.sub(r'\s+', ' ', note_raw)

        note_cleaned = note_cleaned.strip('\'"')

        entities['note_text'] = note_cleaned

        return entities
