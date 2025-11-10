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

        # Pattern 1: Name after 'contact' keyword (e.g., "contact John", "remove contact Met")
        for match in re.finditer(RegexPatterns.NAME_AFTER_CONTACT_PATTERN, text, re.IGNORECASE):
            name = match.group(1)
            # Skip if it's a command word
            if not is_stop_word(name) and name.lower() not in EntityConfig.COMMAND_WORDS:
                entities.append(Entity(
                    text=name,
                    start=match.start(1),
                    end=match.end(1),
                    entity_type='name',
                    confidence=ConfidenceConfig.HEURISTIC_NAME_AFTER_CONTACT_CONFIDENCE,
                    strategy=ExtractionStrategy.HEURISTIC
                ))

        # Pattern 1b: Name before 'contact' keyword (e.g., "delete Alon contact")
        for match in re.finditer(RegexPatterns.NAME_BEFORE_CONTACT_PATTERN, text, re.IGNORECASE):
            name = match.group(1)
            # Filter out command words from the beginning
            words = name.split()
            filtered_words = [w for w in words if w.lower() not in EntityConfig.COMMAND_WORDS and not is_stop_word(w)]

            if filtered_words:
                filtered_name = ' '.join(filtered_words)
                # Calculate new start position
                first_kept_word = filtered_words[0]
                start_offset = name.find(first_kept_word)
                new_start = match.start(1) + start_offset

                entities.append(Entity(
                    text=filtered_name,
                    start=new_start,
                    end=new_start + len(filtered_name),
                    entity_type='name',
                    confidence=ConfidenceConfig.HEURISTIC_NAME_AFTER_CONTACT_CONFIDENCE,
                    strategy=ExtractionStrategy.HEURISTIC
                ))

        # Pattern 2: Single name before possessive (e.g., "David's")
        for match in re.finditer(RegexPatterns.NAME_POSSESSIVE_PATTERN, text):
            name = match.group(1)
            # Skip if it's a command word
            if not is_stop_word(name) and name.lower() not in EntityConfig.COMMAND_WORDS:
                entities.append(Entity(
                    text=name,
                    start=match.start(),
                    end=match.end(),
                    entity_type='name',
                    confidence=ConfidenceConfig.HEURISTIC_NAME_POSSESSIVE_CONFIDENCE,
                    strategy=ExtractionStrategy.HEURISTIC
                ))

        # Pattern 3: Full name (2-3 capitalized words)
        for match in re.finditer(RegexPatterns.NAME_FULL_PATTERN, text):
            name = match.group(1)
            words = name.split()

            # Filter out command words
            filtered_words = [w for w in words if w.lower() not in EntityConfig.COMMAND_WORDS and not is_stop_word(w)]

            if filtered_words:
                # Reconstruct name without command words
                filtered_name = ' '.join(filtered_words)
                # Calculate new start position
                first_kept_word = filtered_words[0]
                start_offset = name.find(first_kept_word)
                new_start = match.start() + start_offset

                entities.append(Entity(
                    text=filtered_name,
                    start=new_start,
                    end=new_start + len(filtered_name),
                    entity_type='name',
                    confidence=ConfidenceConfig.HEURISTIC_NAME_FULL_CONFIDENCE,
                    strategy=ExtractionStrategy.HEURISTIC
                ))

        return entities

    @staticmethod
    def _extract_addresses(text: str) -> List[Entity]:
        entities = []

        # Build dynamic patterns from config
        state_pattern = '|'.join(EntityConfig.US_STATES)
        street_suffixes = '|'.join(EntityConfig.STREET_SUFFIXES)

        # Pattern 1: City, State ZIP (fill placeholder)
        city_state_pattern = RegexPatterns.ADDRESS_CITY_STATE_ZIP_PATTERN.format(state_pattern=state_pattern)
        for match in re.finditer(city_state_pattern, text):
            entities.append(Entity(
                text=match.group(),
                start=match.start(),
                end=match.end(),
                entity_type='address',
                confidence=ConfidenceConfig.HEURISTIC_ADDRESS_CITY_STATE_CONFIDENCE,
                strategy=ExtractionStrategy.HEURISTIC
            ))

        # Pattern 2: Street address patterns (fill placeholder)
        street_pattern = RegexPatterns.ADDRESS_STREET_PATTERN.format(street_suffixes=street_suffixes)
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
