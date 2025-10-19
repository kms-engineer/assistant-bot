import re
from typing import Dict

from .base import EntityValidator


class AddressValidator(EntityValidator):

    def validate(self, entities: Dict) -> Dict:
        if 'address' not in entities or not entities['address']:
            return entities

        address_raw = entities['address'].strip()

        city_match = re.search(r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)$', address_raw)
        if city_match:
            entities['city'] = city_match.group(1)
        else:
            city_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b$'
            match = re.search(city_pattern, address_raw)
            if match:
                potential_city = match.group(1)
                if potential_city.lower() not in ['street', 'road', 'avenue', 'drive', 'lane']:
                    entities['city'] = potential_city

        entities['address'] = re.sub(r'\s+', ' ', address_raw)

        return entities
