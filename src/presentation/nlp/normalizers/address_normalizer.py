import re
from typing import Dict
from src.config import EntityConfig, RegexPatterns


class AddressNormalizer:

    _CITY_PATTERN = re.compile(RegexPatterns.ADDRESS_CITY_PATTERN)

    @staticmethod
    def normalize(entities: Dict) -> Dict:
        if 'address' not in entities or not entities['address']:
            return entities

        address_raw = entities['address'].strip()

        # Try to extract city using pattern from config
        city_match = AddressNormalizer._CITY_PATTERN.search(address_raw)
        if city_match:
            entities['city'] = city_match.group(1)
        else:
            city_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b$'
            match = re.search(city_pattern, address_raw)
            if match:
                potential_city = match.group(1)
                # Exclude common street suffixes from config
                if potential_city.lower() not in EntityConfig.STREET_SUFFIXES_LOWER:
                    entities['city'] = potential_city

        # Normalize whitespace
        entities['address'] = re.sub(r'\s+', ' ', address_raw)

        return entities
