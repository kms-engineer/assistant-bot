import re
from typing import List

from .base import Entity, ExtractionStrategy, is_stop_word

try:
    import phonenumbers
    from phonenumbers import NumberParseException
    HAS_PHONENUMBERS = True
except ImportError:
    HAS_PHONENUMBERS = False

try:
    from email_validator import validate_email, EmailNotValidError
    HAS_EMAIL_VALIDATOR = True
except ImportError:
    HAS_EMAIL_VALIDATOR = False

try:
    import usaddress
    HAS_USADDRESS = True
except ImportError:
    HAS_USADDRESS = False

try:
    import pyap
    HAS_PYAP = True
except ImportError:
    HAS_PYAP = False

try:
    import spacy
    HAS_SPACY = True
    try:
        nlp_spacy = spacy.load("en_core_web_sm")
    except:
        HAS_SPACY = False
        nlp_spacy = None
except ImportError:
    HAS_SPACY = False
    nlp_spacy = None

try:
    from dateutil import parser as date_parser
    HAS_DATEUTIL = True
except ImportError:
    HAS_DATEUTIL = False


class LibraryExtractor:

    @staticmethod
    def extract_all(text: str) -> List[Entity]:
        entities = []

        if HAS_PHONENUMBERS:
            entities.extend(LibraryExtractor._extract_phones(text))

        if HAS_EMAIL_VALIDATOR:
            entities.extend(LibraryExtractor._extract_emails(text))

        if HAS_USADDRESS or HAS_PYAP:
            entities.extend(LibraryExtractor._extract_addresses(text))

        if HAS_SPACY:
            entities.extend(LibraryExtractor._extract_names(text))

        if HAS_DATEUTIL:
            entities.extend(LibraryExtractor._extract_birthdays(text))

        return entities

    @staticmethod
    def _extract_phones(text: str) -> List[Entity]:
        entities = []
        try:
            for match in phonenumbers.PhoneNumberMatcher(text, "US"):
                phone_str = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164)
                entities.append(Entity(
                    text=phone_str.replace('+1', ''),
                    start=match.start,
                    end=match.end,
                    entity_type='phone',
                    confidence=0.95,
                    strategy=ExtractionStrategy.LIBRARY
                ))
        except Exception:
            pass
        return entities

    @staticmethod
    def _extract_emails(text: str) -> List[Entity]:
        entities = []
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        for match in re.finditer(email_pattern, text):
            email_str = match.group()
            try:
                validate_email(email_str)
                entities.append(Entity(
                    text=email_str,
                    start=match.start(),
                    end=match.end(),
                    entity_type='email',
                    confidence=0.95,
                    strategy=ExtractionStrategy.LIBRARY
                ))
            except:
                pass
        return entities

    @staticmethod
    def _extract_addresses(text: str) -> List[Entity]:
        entities = []

        # Try pyap first (better at finding addresses)
        if HAS_PYAP:
            try:
                addresses = pyap.parse(text, country='US')
                for addr in addresses:
                    entities.append(Entity(
                        text=str(addr),
                        start=text.find(str(addr)),
                        end=text.find(str(addr)) + len(str(addr)),
                        entity_type='address',
                        confidence=0.85,
                        strategy=ExtractionStrategy.LIBRARY
                    ))
            except Exception:
                pass

        # Fallback to usaddress
        if HAS_USADDRESS and not entities:
            try:
                parsed, address_type = usaddress.tag(text)
                if address_type in ['Street Address', 'Ambiguous']:
                    address_parts = []
                    for key, value in parsed.items():
                        if key not in ['Recipient', 'NotAddress']:
                            address_parts.append(value)
                    if address_parts:
                        address_str = ' '.join(address_parts)
                        start = text.find(address_str)
                        if start >= 0:
                            entities.append(Entity(
                                text=address_str,
                                start=start,
                                end=start + len(address_str),
                                entity_type='address',
                                confidence=0.80,
                                strategy=ExtractionStrategy.LIBRARY
                            ))
            except Exception:
                pass

        return entities

    @staticmethod
    def _extract_names(text: str) -> List[Entity]:
        entities = []
        try:
            doc = nlp_spacy(text)
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    # Remove possessive 's from name
                    name_text = ent.text
                    name_end = ent.end_char
                    if name_text.endswith("'s"):
                        name_text = name_text[:-2]
                        name_end -= 2

                    if name_text and not is_stop_word(name_text):
                        entities.append(Entity(
                            text=name_text,
                            start=ent.start_char,
                            end=name_end,
                            entity_type='name',
                            confidence=0.80,
                            strategy=ExtractionStrategy.LIBRARY
                        ))
        except Exception:
            pass
        return entities

    @staticmethod
    def _extract_birthdays(text: str) -> List[Entity]:
        entities = []
        date_patterns = [
            r'\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b',
            r'\b\d{4}[./-]\d{1,2}[./-]\d{1,2}\b',
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b',
        ]

        for pattern in date_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                date_str = match.group()
                try:
                    parsed_date = date_parser.parse(date_str, fuzzy=False)
                    entities.append(Entity(
                        text=date_str,
                        start=match.start(),
                        end=match.end(),
                        entity_type='birthday',
                        confidence=0.85,
                        strategy=ExtractionStrategy.LIBRARY
                    ))
                    break  # Take first valid date
                except:
                    pass

        return entities

    @staticmethod
    def get_available_libraries() -> dict:
        return {
            'phonenumbers': HAS_PHONENUMBERS,
            'email_validator': HAS_EMAIL_VALIDATOR,
            'usaddress': HAS_USADDRESS,
            'pyap': HAS_PYAP,
            'spacy': HAS_SPACY,
            'dateutil': HAS_DATEUTIL,
        }
