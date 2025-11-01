import re
from typing import Dict
from src.config import EntityConfig, RegexPatterns


class AddressNormalizer:

    _CITY_PATTERN = re.compile(RegexPatterns.ADDRESS_CITY_PATTERN)

    @staticmethod
    def normalize(entities: Dict) -> Dict:
        if 'address' not in entities or not entities['address']:
            return entities

        # First, strip leading/trailing whitespace, then collapse internal whitespace.
        address_cleaned = re.sub(r'\s+', ' ', entities['address'].strip())
        entities['address'] = address_cleaned

        # Try to extract city using pattern from config
        city_match = AddressNormalizer._CITY_PATTERN.search(address_cleaned)
        if city_match:
            entities['city'] = city_match.group(1)
        else:
            city_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b$'
            match = re.search(city_pattern, address_cleaned)
            if match:
                potential_city = match.group(1)
                # Exclude common street suffixes from config
                if potential_city.lower() not in EntityConfig.STREET_SUFFIXES_LOWER:
                    entities['city'] = potential_city

        return entities
