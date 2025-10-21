import re
from typing import Dict
from .string_validator import StringValidator


class TagValidator:
    MAX_LENGTH = 50

    @staticmethod
    def validate(value):
        # Check if value is a string
        if not StringValidator.is_string(value):
            return "Tag must be a string"

        # Check if empty or whitespace
        if StringValidator.is_empty(value):
            return "Tag cannot be empty"

        # Check max length
        if not StringValidator.has_max_length(value, TagValidator.MAX_LENGTH):
            return f"Tag too long (max {TagValidator.MAX_LENGTH} characters)"

        return True

    @staticmethod
    def validate_and_raise(value: str) -> None:
        result = TagValidator.validate(value)
        if result is not True:
            raise ValueError(result)

    @staticmethod
    def normalize_for_nlp(entities: Dict) -> Dict:
        if 'tag' not in entities or not entities['tag']:
            return entities

        tag_raw = entities['tag'].strip()

        # Add # prefix if missing
        if not tag_raw.startswith('#'):
            tag_raw = '#' + tag_raw

        # Remove invalid characters (keep only word chars and #)
        tag_raw = re.sub(r'[^\w#]', '', tag_raw)

        entities['tag'] = tag_raw
        return entities
