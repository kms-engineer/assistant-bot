import re
from typing import Dict
from src.config import RegexPatterns


class TagNormalizer:

    @staticmethod
    def normalize(entities: Dict) -> Dict:
        if "tag" not in entities or not entities["tag"]:
            return entities

        tag_raw = entities["tag"].strip()

        # Add # prefix if missing
        if not tag_raw.startswith("#"):
            tag_raw = "#" + tag_raw

        # Remove invalid characters using pattern from config
        tag_raw = re.sub(RegexPatterns.TAG_INVALID_CHAR_PATTERN, "", tag_raw)

        entities["tag"] = tag_raw
        return entities
