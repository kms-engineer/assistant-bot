import re
from typing import List

from .base import Entity, ExtractionStrategy, is_stop_word
from src.config import ModelConfig, RegexPatterns

try:
    import phonenumbers
    from phonenumbers import NumberParseException
    HAS_PHONENUMBERS = True
except ImportError:
    phonenumbers = None
    NumberParseException = Exception
    HAS_PHONENUMBERS = False

try:
    from email_validator import validate_email, EmailNotValidError
    HAS_EMAIL_VALIDATOR = True
except ImportError:
    validate_email = None
    EmailNotValidError = Exception
    HAS_EMAIL_VALIDATOR = False

try:
    import usaddress
    HAS_USADDRESS = True
except ImportError:
    usaddress = None
    HAS_USADDRESS = False

try:
    import pyap
    HAS_PYAP = True
except ImportError:
    pyap = None
    HAS_PYAP = False

try:
    import spacy
    HAS_SPACY = True
    try:
        nlp_spacy = spacy.load(ModelConfig.SPACY_MODEL_NAME)
    except (OSError, IOError) as e:
        HAS_SPACY = False
        nlp_spacy = None
except ImportError:
    spacy = None
    HAS_SPACY = False
    nlp_spacy = None

try:
    from dateutil import parser as date_parser
    HAS_DATEUTIL = True
except ImportError:
    date_parser = None
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
        if not phonenumbers:
            return entities
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
        except (NumberParseException, AttributeError, ValueError) as e:
            # Ignore parse errors for invalid phone numbers
            pass
        return entities

    @staticmethod
    def _extract_emails(text: str) -> List[Entity]:
        entities = []
        if not validate_email:
            return entities
        for match in re.finditer(RegexPatterns.EMAIL_PATTERN, text):
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
            except (EmailNotValidError, ValueError, TypeError):
                # Ignore invalid emails
                pass
        return entities

    @staticmethod
    def _extract_addresses(text: str) -> List[Entity]:
        entities = []

        # Try pyap first (better at finding addresses)
        if HAS_PYAP and pyap:
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
            except (ValueError, AttributeError, TypeError):
                # Ignore parsing errors
                pass

        # Fallback to usaddress
        if HAS_USADDRESS and usaddress and not entities:
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
            except (ValueError, AttributeError, TypeError, KeyError):
                # Ignore parsing errors
                pass

        return entities

    @staticmethod
    def _extract_names(text: str) -> List[Entity]:
        entities = []
        if not nlp_spacy:
            return entities
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
        except (ValueError, AttributeError, TypeError):
            # Ignore spacy processing errors
            pass
        return entities

    @staticmethod
    def _extract_birthdays(text: str) -> List[Entity]:
        entities = []
        if not date_parser:
            return entities

        date_patterns = [
            RegexPatterns.DATE_PATTERN_SLASH_DOT,
            RegexPatterns.DATE_PATTERN_ISO,
            RegexPatterns.DATE_PATTERN_MONTH_NAME,
        ]

        for pattern in date_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                date_str = match.group()
                try:
                    # Validate date by parsing (we don't use the result, just check if valid)
                    _ = date_parser.parse(date_str, fuzzy=False)
                    entities.append(Entity(
                        text=date_str,
                        start=match.start(),
                        end=match.end(),
                        entity_type='birthday',
                        confidence=0.85,
                        strategy=ExtractionStrategy.LIBRARY
                    ))
                    break  # Take first valid date
                except (ValueError, TypeError, OverflowError):
                    # Ignore invalid date formats
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
