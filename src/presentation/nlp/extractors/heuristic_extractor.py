import re
from typing import List
from .base import Entity, ExtractionStrategy, is_stop_word
from src.config import EntityConfig, ConfidenceConfig, RegexPatterns


class HeuristicExtractor:

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
        for match in re.finditer(RegexPatterns.NAME_POSSESSIVE_PATTERN, text):
            name = match.group(1)
            if not is_stop_word(name):
                entities.append(Entity(
                    text=name,
                    start=match.start(),
                    end=match.end(),
                    entity_type='name',
                    confidence=ConfidenceConfig.HEURISTIC_NAME_POSSESSIVE_CONFIDENCE,
                    strategy=ExtractionStrategy.HEURISTIC
                ))

        # Pattern 2: Full name (2-3 capitalized words)
        for match in re.finditer(RegexPatterns.NAME_FULL_PATTERN, text):
            name = match.group(1)
            # Filter out if all words are stop words
            words = name.split()
            if not all(is_stop_word(word) for word in words):
                entities.append(Entity(
                    text=name,
                    start=match.start(),
                    end=match.end(),
                    entity_type='name',
                    confidence=ConfidenceConfig.HEURISTIC_NAME_FULL_CONFIDENCE,
                    strategy=ExtractionStrategy.HEURISTIC
                ))

        return entities

    @staticmethod
    def _extract_addresses(text: str) -> List[Entity]:
        entities = []
        state_pattern = '|'.join(EntityConfig.US_STATES)

        # Pattern 1: City, State ZIP
        pattern1 = rf'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s*({state_pattern})\s+(\d{{5}}(?:-\d{{4}})?)\b'
        for match in re.finditer(pattern1, text):
            entities.append(Entity(
                text=match.group(),
                start=match.start(),
                end=match.end(),
                entity_type='address',
                confidence=ConfidenceConfig.HEURISTIC_ADDRESS_CITY_STATE_CONFIDENCE,
                strategy=ExtractionStrategy.HEURISTIC
            ))

        # Pattern 2: Street address patterns
        street_suffixes = '|'.join(EntityConfig.STREET_SUFFIXES)
        street_pattern = rf'\b\d+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:{street_suffixes})\b'
        for match in re.finditer(street_pattern, text, re.IGNORECASE):
            entities.append(Entity(
                text=match.group(),
                start=match.start(),
                end=match.end(),
                entity_type='address',
                confidence=ConfidenceConfig.HEURISTIC_ADDRESS_STREET_CONFIDENCE,
                strategy=ExtractionStrategy.HEURISTIC
            ))

        return entities
