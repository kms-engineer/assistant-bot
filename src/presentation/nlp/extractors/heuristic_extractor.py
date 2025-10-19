import re
from typing import List
from .base import Entity, ExtractionStrategy, is_stop_word


class HeuristicExtractor:

    # US states abbreviations
    US_STATES = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL',
                 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT',
                 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',
                 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

    @staticmethod
    def extract_all(text: str) -> List[Entity]:
        entities = []
        entities.extend(HeuristicExtractor._extract_names(text))
        entities.extend(HeuristicExtractor._extract_addresses(text))
        return entities

    @staticmethod
    def _extract_names(text: str) -> List[Entity]:
        entities = []

        # Pattern 1: Single name before possessive (e.g., "David's")
        name_possessive_pattern = r'\b([A-Z][a-z]+)(?=\'s\b)'
        for match in re.finditer(name_possessive_pattern, text):
            name = match.group(1)
            if not is_stop_word(name):
                entities.append(Entity(
                    text=name,
                    start=match.start(),
                    end=match.end(),
                    entity_type='name',
                    confidence=0.65,
                    strategy=ExtractionStrategy.HEURISTIC
                ))

        # Pattern 2: Full name (2-3 capitalized words)
        full_name_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})\b'
        for match in re.finditer(full_name_pattern, text):
            name = match.group(1)
            # Filter out if all words are stop words
            words = name.split()
            if not all(is_stop_word(word) for word in words):
                entities.append(Entity(
                    text=name,
                    start=match.start(),
                    end=match.end(),
                    entity_type='name',
                    confidence=0.60,
                    strategy=ExtractionStrategy.HEURISTIC
                ))

        return entities

    @staticmethod
    def _extract_addresses(text: str) -> List[Entity]:
        entities = []
        state_pattern = '|'.join(HeuristicExtractor.US_STATES)

        # Pattern 1: City, State ZIP
        pattern1 = rf'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s*({state_pattern})\s+(\d{{5}}(?:-\d{{4}})?)\b'
        for match in re.finditer(pattern1, text):
            entities.append(Entity(
                text=match.group(),
                start=match.start(),
                end=match.end(),
                entity_type='address',
                confidence=0.75,
                strategy=ExtractionStrategy.HEURISTIC
            ))

        # Pattern 2: Street address patterns
        street_pattern = r'\b\d+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln)\b'
        for match in re.finditer(street_pattern, text, re.IGNORECASE):
            entities.append(Entity(
                text=match.group(),
                start=match.start(),
                end=match.end(),
                entity_type='address',
                confidence=0.70,
                strategy=ExtractionStrategy.HEURISTIC
            ))

        return entities
