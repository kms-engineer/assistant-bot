import re
from typing import List

from .base import Entity, ExtractionStrategy
from src.config import RegexPatterns, ConfidenceConfig, EntityConfig


class RegexExtractor:

    def __init__(self):
        self._compile_patterns()

    def _compile_patterns(self):
        # Compile patterns from config
        self.phone_pattern = re.compile(
            r'\b(?:\+?1[-.]?)?'  # Optional country code
            r'(?:\(?\d{3}\)?[-.\s]?)?'  # Area code
            r'\d{3}[-.\s]?\d{4}\b'  # Main number
        )

        self.email_pattern = re.compile(RegexPatterns.EMAIL_PATTERN)
        self.birthday_pattern = re.compile(
            r'\b(?:'
            r'\d{1,2}[./-]\d{1,2}[./-]\d{2,4}|'  # DD.MM.YYYY, DD/MM/YYYY, etc.
            r'\d{4}[./-]\d{1,2}[./-]\d{1,2}|'  # YYYY-MM-DD
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}|'  # Month DD, YYYY
            r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}'  # DD Month YYYY
            r')\b'
        )
        self.tag_pattern = re.compile(RegexPatterns.TAG_PATTERN)
        self.uuid_pattern = re.compile(RegexPatterns.UUID_PATTERN, re.IGNORECASE)

    def extract_all(self, text: str) -> List[Entity]:
        entities = []

        # Phone
        phone_match = self.phone_pattern.search(text)
        if phone_match:
            entities.append(Entity(
                text=phone_match.group(),
                start=phone_match.start(),
                end=phone_match.end(),
                entity_type='phone',
                confidence=ConfidenceConfig.REGEX_PHONE_CONFIDENCE,
                strategy=ExtractionStrategy.REGEX
            ))

        # Email
        email_match = self.email_pattern.search(text)
        if email_match:
            entities.append(Entity(
                text=email_match.group(),
                start=email_match.start(),
                end=email_match.end(),
                entity_type='email',
                confidence=ConfidenceConfig.REGEX_EMAIL_CONFIDENCE,
                strategy=ExtractionStrategy.REGEX
            ))

        # Birthday
        birthday_match = self.birthday_pattern.search(text)
        if birthday_match:
            entities.append(Entity(
                text=birthday_match.group(),
                start=birthday_match.start(),
                end=birthday_match.end(),
                entity_type='birthday',
                confidence=ConfidenceConfig.REGEX_BIRTHDAY_CONFIDENCE,
                strategy=ExtractionStrategy.REGEX
            ))

        # Tags
        for tag_match in self.tag_pattern.finditer(text):
            entities.append(Entity(
                text=tag_match.group(),
                start=tag_match.start(),
                end=tag_match.end(),
                entity_type='tag',
                confidence=ConfidenceConfig.REGEX_TAG_CONFIDENCE,
                strategy=ExtractionStrategy.REGEX
            ))

        # UUID (for IDs)
        uuid_match = self.uuid_pattern.search(text)
        if uuid_match:
            entities.append(Entity(
                text=uuid_match.group(),
                start=uuid_match.start(),
                end=uuid_match.end(),
                entity_type='id',
                confidence=ConfidenceConfig.REGEX_ID_CONFIDENCE,
                strategy=ExtractionStrategy.REGEX
            ))

        # Note text extraction
        note_text = self._extract_note_text(text)
        if note_text:
            start = text.find(note_text)
            entities.append(Entity(
                text=note_text,
                start=start,
                end=start + len(note_text),
                entity_type='note_text',
                confidence=ConfidenceConfig.REGEX_NOTE_TEXT_CONFIDENCE,
                strategy=ExtractionStrategy.REGEX
            ))

        return entities

    def _extract_note_text(self, text: str) -> str:
        # Check for quoted text first (highest priority)
        quoted_patterns = [
            r'["\']([^"\']{2,})["\']',  # Standard quotes
            r'[\u2018\u2019]([^\u2018\u2019]{2,})[\u2018\u2019]',  # Smart single quotes
            r'[\u201C\u201D]([^\u201C\u201D]{2,})[\u201C\u201D]',  # Smart double quotes
        ]

        for pattern in quoted_patterns:
            quoted_match = re.search(pattern, text)
            if quoted_match:
                return quoted_match.group(1).strip()

        # Strategy: Remove command phrases progressively
        cleaned = text

        # Step 1: Remove command phrases at the beginning
        command_patterns = [
            r'^\s*add\s+a?\s*note\s+',
            r'^\s*create\s+a?\s*note\s+',
            r'^\s*new\s+note\s+',
            r'^\s*make\s+a?\s*note\s+',
            r'^\s*write\s+a?\s*note\s+',
            r'^\s*note\s*:\s*',
            r'^\s*note\s+about\s+',
            r'^\s*note\s+that\s+',
            r'^\s*note\s+',
        ]

        for pattern in command_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
            if cleaned != text:  # If something was removed, stop
                break

        # Step 2: Remove hashtags
        tag_pattern = r'#\w+'
        cleaned = re.sub(tag_pattern, '', cleaned)

        # Step 3: Clean up
        cleaned = cleaned.strip()
        cleaned = re.sub(r'\s+', ' ', cleaned)  # Normalize whitespace
        cleaned = re.sub(r'^\s*[:;,.\\-]\s*', '', cleaned)  # Remove leading punctuation
        cleaned = re.sub(r'\s*[:;,.\\-]\s*$', '', cleaned)  # Remove trailing punctuation

        # Remove any remaining quotes
        cleaned = cleaned.strip('\'"''')

        # Final validation using config
        alphanumeric = re.sub(r'[^\w\s]', '', cleaned)
        if (len(alphanumeric) >= EntityConfig.NOTE_MIN_ALPHANUMERIC and
            (len(cleaned) >= EntityConfig.NOTE_MIN_LENGTH_OR_WORDS or len(cleaned.split()) >= 1)):
            return cleaned

        return None
