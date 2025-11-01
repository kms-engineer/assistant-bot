import re
from typing import Dict


class NameNormalizer:

    @staticmethod
    def normalize(entities: Dict) -> Dict:
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
            if '_validation_errors' not in entities:
                entities['_validation_errors'] = []
            entities['_validation_errors'].append(f"Name too short: {name_cleaned}")
        else:
            entities['_name_valid'] = True

        return entities
