import re

from typing import List

from .base import Entity, ExtractionStrategy
from src.config import RegexPatterns, ConfidenceConfig, EntityConfig


class RegexExtractor:

    def __init__(self):
        self._compile_patterns()

    def _compile_patterns(self):
        # Compile patterns from config
        self.phone_pattern = re.compile(RegexPatterns.PHONE_PATTERN_ADVANCED)
        self.email_pattern = re.compile(RegexPatterns.EMAIL_PATTERN)
        self.birthday_pattern = re.compile(RegexPatterns.BIRTHDAY_PATTERN_COMBINED)
        self.tag_pattern = re.compile(RegexPatterns.TAG_PATTERN)
        self.uuid_pattern = re.compile(RegexPatterns.UUID_PATTERN, re.IGNORECASE)
        self.days_pattern = re.compile(RegexPatterns.DAYS_PATTERN, re.IGNORECASE)

    def extract_all(self, text: str) -> List[Entity]:
        entities = []

        # Phone - extract ALL phone numbers (for edit_phone intent with old_phone and new_phone)
        phone_matches = list(self.phone_pattern.finditer(text))
        if phone_matches:
            if len(phone_matches) == 1:
                # Single phone - use generic 'phone' type
                match = phone_matches[0]
                entities.append(
                    Entity(
                        text=match.group(),
                        start=match.start(),
                        end=match.end(),
                        entity_type="phone",
                        confidence=ConfidenceConfig.REGEX_PHONE_CONFIDENCE,
                        strategy=ExtractionStrategy.REGEX,
                    )
                )
            elif len(phone_matches) >= 2:
                # Multiple phones - label first as old_phone, second as new_phone
                old_match = phone_matches[0]
                entities.append(
                    Entity(
                        text=old_match.group(),
                        start=old_match.start(),
                        end=old_match.end(),
                        entity_type="old_phone",
                        confidence=ConfidenceConfig.REGEX_PHONE_CONFIDENCE,
                        strategy=ExtractionStrategy.REGEX,
                    )
                )

                new_match = phone_matches[1]
                entities.append(
                    Entity(
                        text=new_match.group(),
                        start=new_match.start(),
                        end=new_match.end(),
                        entity_type="new_phone",
                        confidence=ConfidenceConfig.REGEX_PHONE_CONFIDENCE,
                        strategy=ExtractionStrategy.REGEX,
                    )
                )

        # Email
        email_match = self.email_pattern.search(text)
        if email_match:
            entities.append(
                Entity(
                    text=email_match.group(),
                    start=email_match.start(),
                    end=email_match.end(),
                    entity_type="email",
                    confidence=ConfidenceConfig.REGEX_EMAIL_CONFIDENCE,
                    strategy=ExtractionStrategy.REGEX,
                )
            )

        # Birthday
        birthday_match = self.birthday_pattern.search(text)
        if birthday_match:
            entities.append(
                Entity(
                    text=birthday_match.group(),
                    start=birthday_match.start(),
                    end=birthday_match.end(),
                    entity_type="birthday",
                    confidence=ConfidenceConfig.REGEX_BIRTHDAY_CONFIDENCE,
                    strategy=ExtractionStrategy.REGEX,
                )
            )

        # Tags
        for tag_match in self.tag_pattern.finditer(text):
            entities.append(
                Entity(
                    text=tag_match.group(),
                    start=tag_match.start(),
                    end=tag_match.end(),
                    entity_type="tag",
                    confidence=ConfidenceConfig.REGEX_TAG_CONFIDENCE,
                    strategy=ExtractionStrategy.REGEX,
                )
            )

        # UUID (for IDs)
        uuid_match = self.uuid_pattern.search(text)
        if uuid_match:
            entities.append(
                Entity(
                    text=uuid_match.group(),
                    start=uuid_match.start(),
                    end=uuid_match.end(),
                    entity_type="id",
                    confidence=ConfidenceConfig.REGEX_ID_CONFIDENCE,
                    strategy=ExtractionStrategy.REGEX,
                )
            )

        # Days (for birthday/birthdays commands)
        days_match = self.days_pattern.search(text)
        if days_match:
            entities.append(
                Entity(
                    text=days_match.group(1),  # Extract just the number
                    start=days_match.start(1),
                    end=days_match.end(1),
                    entity_type="days",
                    confidence=ConfidenceConfig.REGEX_DAYS_CONFIDENCE,
                    strategy=ExtractionStrategy.REGEX,
                )
            )

        # Note text extraction
        note_text = RegexExtractor._extract_note_text(text)
        if note_text:
            start = text.find(note_text)
            entities.append(
                Entity(
                    text=note_text,
                    start=start,
                    end=start + len(note_text),
                    entity_type="note_text",
                    confidence=ConfidenceConfig.REGEX_NOTE_TEXT_CONFIDENCE,
                    strategy=ExtractionStrategy.REGEX,
                )
            )

        return entities

    @staticmethod
    def _extract_note_text(text: str) -> str | None:
        # Check for quoted text first (highest priority)
        for pattern in RegexPatterns.QUOTED_PATTERNS_EXTENDED:
            quoted_match = re.search(pattern, text)
            if quoted_match:
                return quoted_match.group(1).strip()

        # Strategy: Remove command phrases progressively
        cleaned = text

        # Step 1: Remove command phrases at the beginning
        for pattern in RegexPatterns.NOTE_COMMAND_PATTERNS:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
            if cleaned != text:  # If something was removed, stop
                break

        # Step 2: Remove hashtags
        cleaned = re.sub(RegexPatterns.TAG_PATTERN, "", cleaned)

        # Step 3: Clean up
        cleaned = cleaned.strip()
        cleaned = re.sub(RegexPatterns.WHITESPACE_NORMALIZE_PATTERN, " ", cleaned)
        cleaned = re.sub(RegexPatterns.LEADING_PUNCTUATION_PATTERN, "", cleaned)
        cleaned = re.sub(RegexPatterns.TRAILING_PUNCTUATION_PATTERN, "", cleaned)

        # Remove any remaining quotes
        cleaned = cleaned.strip("'\"" "")

        # Final validation using config
        alphanumeric = re.sub(r"[^\w\s]", "", cleaned)
        if len(alphanumeric) >= EntityConfig.NOTE_MIN_ALPHANUMERIC and (
            len(cleaned) >= EntityConfig.NOTE_MIN_LENGTH_OR_WORDS
            or len(cleaned.split()) >= 1
        ):
            return cleaned

        return None
