import re
from typing import Dict
from src.config import ValidationConfig, RegexPatterns


class TagValidator:
    MAX_LENGTH = ValidationConfig.TAG_MAX_LENGTH

    @staticmethod
    def validate(value):
        # Check if value is a string
        if not isinstance(value, str):
            return "Tag must be a string"

        # Check if empty or whitespace
        if not value or len(value.strip()) == 0:
            return "Tag cannot be empty"

        # Check max length
        if len(value) > TagValidator.MAX_LENGTH:
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

        # Remove invalid characters using pattern from config
        tag_raw = re.sub(RegexPatterns.TAG_INVALID_CHAR_PATTERN, '', tag_raw)

        entities['tag'] = tag_raw
        return entities
