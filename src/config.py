

# =============================================================================
# NLP Configuration
# =============================================================================

class NLPConfig:

    # Intent classification thresholds
    INTENT_CONFIDENCE_THRESHOLD = 0.6
    """Minimum confidence for accepting intent classification result."""

    # Entity extraction thresholds
    ENTITY_CONFIDENCE_THRESHOLD = 0.5
    """Minimum confidence for accepting entity extraction result."""

    # Entity merging (confidence-based selection between regex and NER)
    CONFIDENCE_OVERRIDE_THRESHOLD = 0.3
    """If confidence difference > 0.3, override preference and use higher confidence source."""

    # User input processing
    LOW_CONFIDENCE_THRESHOLD = 0.55
    """If confidence < 0.55, suggest alternative commands to user."""

    # Command suggestion
    COMMAND_SUGGESTION_CUTOFF = 0.6
    """Fuzzy matching cutoff for command suggestions (0.0 to 1.0)."""

    # Default region for phone number parsing
    DEFAULT_REGION = "US"
    """Default region code for phone number validation and formatting."""


# =============================================================================
# Validation Configuration
# =============================================================================

class ValidationConfig:

    # Name validation
    NAME_MIN_LENGTH = 2
    """Minimum length for contact names."""

    NAME_MAX_LENGTH = 50
    """Maximum length for contact names."""

    # Address validation
    ADDRESS_MIN_LENGTH = 5
    """Minimum length for addresses."""

    ADDRESS_MAX_LENGTH = 200
    """Maximum length for addresses."""

    # Tag validation
    TAG_MAX_LENGTH = 50
    """Maximum length for note tags."""

    # Phone validation
    PHONE_MIN_DIGITS = 10
    """Minimum number of digits in a phone number."""

    PHONE_MAX_DIGITS = 15
    """Maximum number of digits in a phone number."""


# =============================================================================
# UI Configuration
# =============================================================================

class UIConfig:

    # Command suggestion in classic mode
    CLASSIC_COMMAND_SUGGESTION_CUTOFF = 0.6
    """Fuzzy matching cutoff for command suggestions in classic mode."""


# =============================================================================
# Storage Configuration
# =============================================================================

class StorageConfig:

    # Default storage type can be configured here if needed
    # DEFAULT_STORAGE_TYPE = StorageType.SQLITE
    pass


# =============================================================================
# Intent Configuration
# =============================================================================

class IntentConfig:

    # All supported intent labels
    INTENT_LABELS = [
        "add_contact", "edit_phone", "edit_email", "edit_address", "delete_contact",
        "list_all_contacts", "search_contacts", "add_birthday", "list_birthdays",
        "add_note", "edit_note", "delete_note", "show_notes", "add_note_tag",
        "remove_note_tag", "search_notes_text", "search_notes_by_tag",
        "hello", "help", "exit"
    ]
    """Complete list of all supported intent labels."""

    # Intent to command mapping
    INTENT_TO_COMMAND_MAP = {
        'add_contact': 'add',
        'edit_phone': 'change',
        'edit_email': 'edit-email',
        'edit_address': 'edit-address',
        'delete_contact': 'delete-contact',
        'list_all_contacts': 'all',
        'search_contacts': 'search',
        'add_birthday': 'add-birthday',
        'list_birthdays': 'birthdays',
        'add_note': 'add-note',
        'edit_note': 'edit-note',
        'delete_note': 'delete-note',
        'show_notes': 'show-notes',
        'add_note_tag': 'add-tag',
        'remove_note_tag': 'remove-tag',
        'search_notes_text': 'search-notes',
        'search_notes_by_tag': 'search-by-tag',
        'hello': 'hello',
        'help': 'help',
        'exit': 'exit'
    }
    """Maps intent labels to corresponding command names."""

    # Intent requirements for entity validation
    INTENT_REQUIREMENTS = {
        "add_contact": {
            "required": ["name"],
            "optional": ["phone", "email", "address", "birthday"]
        },
        "edit_phone": {
            "required": ["name", "phone"],
            "optional": []
        },
        "edit_email": {
            "required": ["name", "email"],
            "optional": []
        },
        "edit_address": {
            "required": ["name", "address"],
            "optional": []
        },
        "delete_contact": {
            "required": ["name"],
            "optional": []
        },
        "list_all_contacts": {
            "required": [],
            "optional": []
        },
        "search_contacts": {
            "required": ["name"],
            "optional": []
        },
        "add_birthday": {
            "required": ["name", "birthday"],
            "optional": []
        },
        "list_birthdays": {
            "required": [],
            "optional": ["days"]
        },
        "add_note": {
            "required": ["name", "note_text"],
            "optional": []
        },
        "edit_note": {
            "required": ["name", "id", "note_text"],
            "optional": []
        },
        "delete_note": {
            "required": ["name", "id"],
            "optional": []
        },
        "show_notes": {
            "required": ["name"],
            "optional": []
        },
        "add_note_tag": {
            "required": ["name", "id", "tag"],
            "optional": []
        },
        "remove_note_tag": {
            "required": ["name", "id", "tag"],
            "optional": []
        },
        "search_notes_text": {
            "required": ["note_text"],
            "optional": ["name"]
        },
        "search_notes_by_tag": {
            "required": ["tag"],
            "optional": ["name"]
        },
        "hello": {
            "required": [],
            "optional": []
        },
        "help": {
            "required": [],
            "optional": []
        },
        "exit": {
            "required": [],
            "optional": []
        }
    }
    """Required and optional entities for each intent."""

    # Confidence normalization for keyword-based intent classification
    KEYWORD_CONFIDENCE_MIN = 0.5
    """Minimum confidence value for keyword-based intent classification."""

    KEYWORD_CONFIDENCE_MAX = 0.7
    """Maximum confidence value for keyword-based intent classification."""

    # Default intent fallback
    DEFAULT_INTENT = "help"
    """Default intent when no match is found."""

    DEFAULT_INTENT_CONFIDENCE = 0.3
    """Default confidence for fallback intent."""


# =============================================================================
# Entity Configuration
# =============================================================================

class EntityConfig:

    # Entity labels (IOB2 format)
    ENTITY_LABELS = [
        "O", "B-NAME", "I-NAME", "B-PHONE", "I-PHONE", "B-EMAIL", "I-EMAIL",
        "B-ADDRESS", "I-ADDRESS", "B-BIRTHDAY", "I-BIRTHDAY", "B-TAG", "I-TAG",
        "B-NOTE_TEXT", "I-NOTE_TEXT", "B-ID", "I-ID", "B-DAYS", "I-DAYS"
    ]
    """Complete list of entity labels in IOB2 format."""

    # Entity field preferences (regex vs NER)
    REGEX_PREFERRED_FIELDS = {'phone', 'email', 'birthday', 'tag', 'id'}
    """Entity types that prefer regex-based extraction over NER."""

    NER_PREFERRED_FIELDS = {'name', 'address', 'note_text'}
    """Entity types that prefer NER-based extraction over regex."""

    # Default confidence scores for merging entities
    DEFAULT_REGEX_CONFIDENCE = 1.0
    """Default confidence for regex-matched entities when no value present."""

    DEFAULT_REGEX_NO_MATCH_CONFIDENCE = 0.0
    """Default confidence when regex doesn't match."""

    DEFAULT_NER_CONFIDENCE = 0.5
    """Default confidence for NER-matched entities when no value present."""

    DEFAULT_NER_NO_MATCH_CONFIDENCE = 0.0
    """Default confidence when NER doesn't match."""

    # Entity merging threshold
    ENTITY_MERGE_THRESHOLD = 0.5
    """Minimum confidence for including entity in merged result."""

    # Default entity confidence for simple extraction
    DEFAULT_ENTITY_CONFIDENCE = 0.5
    """Default confidence when no specific confidence is calculated."""

    # Stop words for entity extraction
    STOP_WORDS = {
        'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'should', 'could', 'may', 'might', 'must', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
    }
    """Common stop words to exclude from entity extraction."""

    # US States for address extraction
    US_STATES = {
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
    }
    """US state abbreviations for address parsing."""

    # Street suffixes for address validation
    STREET_SUFFIXES = ['Street', 'St', 'Avenue', 'Ave', 'Road', 'Rd', 'Drive', 'Dr', 'Lane', 'Ln', 'Boulevard', 'Blvd']
    """Common street address suffixes."""

    STREET_SUFFIXES_LOWER = ['street', 'road', 'avenue', 'drive', 'lane']
    """Lowercase street suffixes for validation."""

    # Minimum lengths for note text validation
    NOTE_MIN_ALPHANUMERIC = 2
    """Minimum number of alphanumeric characters for valid note text."""

    NOTE_MIN_LENGTH_OR_WORDS = 3
    """Minimum cleaned text length, or 1 word minimum."""


# =============================================================================
# Model Configuration
# =============================================================================

class ModelConfig:

    # NLP model names
    ROBERTA_MODEL_NAME = "roberta-base"
    """Model name for RoBERTa-based models (intent classifier and NER)."""

    SPACY_MODEL_NAME = "en_core_web_sm"
    """Spacy model name for entity extraction."""

    # Tokenizer settings
    TOKENIZER_MAX_LENGTH = 128
    """Maximum length for tokenizer input."""

    # Spacy entity labels
    SPACY_PERSON_LABEL = "PERSON"
    """Spacy entity label for person names."""


# =============================================================================
# Confidence Score Configuration
# =============================================================================

class ConfidenceConfig:

    # Regex extractor confidence scores
    REGEX_PHONE_CONFIDENCE = 0.75
    """Confidence score for phone numbers extracted via regex."""

    REGEX_EMAIL_CONFIDENCE = 0.80
    """Confidence score for emails extracted via regex."""

    REGEX_BIRTHDAY_CONFIDENCE = 0.70
    """Confidence score for birthdays extracted via regex."""

    REGEX_TAG_CONFIDENCE = 0.95
    """Confidence score for tags extracted via regex."""

    REGEX_ID_CONFIDENCE = 1.0
    """Confidence score for UUIDs/IDs extracted via regex."""

    REGEX_NOTE_TEXT_CONFIDENCE = 0.75
    """Confidence score for note text extracted via regex."""

    # Heuristic extractor confidence scores
    HEURISTIC_NAME_POSSESSIVE_CONFIDENCE = 0.65
    """Confidence score for names extracted via possessive pattern."""

    HEURISTIC_NAME_FULL_CONFIDENCE = 0.60
    """Confidence score for full names extracted via heuristic."""

    HEURISTIC_ADDRESS_CITY_STATE_CONFIDENCE = 0.75
    """Confidence score for city/state/zip addresses extracted via heuristic."""

    HEURISTIC_ADDRESS_STREET_CONFIDENCE = 0.70
    """Confidence score for street addresses extracted via heuristic."""

    # Library extractor confidence scores
    LIBRARY_PHONE_CONFIDENCE = 0.95
    """Confidence score for phone numbers extracted via phonenumbers library."""

    LIBRARY_EMAIL_CONFIDENCE = 0.95
    """Confidence score for emails extracted via email_validator library."""

    LIBRARY_ADDRESS_PYAP_CONFIDENCE = 0.85
    """Confidence score for addresses extracted via pyap library."""

    LIBRARY_ADDRESS_USADDRESS_CONFIDENCE = 0.80
    """Confidence score for addresses extracted via usaddress library."""

    LIBRARY_NAME_SPACY_CONFIDENCE = 0.80
    """Confidence score for names extracted via spacy."""

    LIBRARY_BIRTHDAY_DATEUTIL_CONFIDENCE = 0.85
    """Confidence score for birthdays extracted via dateutil."""

    # Template parser confidence scores
    TEMPLATE_BASE_CONFIDENCE = 0.65
    """Base confidence score for template-based parsing."""

    TEMPLATE_HIGH_CONFIDENCE = 0.70
    """High confidence score for template-based parsing."""


# =============================================================================
# Regex Patterns Configuration
# =============================================================================

class RegexPatterns:

    # Phone number patterns
    PHONE_PATTERN = r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
    """Regex pattern for matching phone numbers (US format)."""

    # Email patterns
    EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    """Regex pattern for matching email addresses."""

    # Birthday/date patterns
    BIRTHDAY_PATTERN = r'\b\d{1,2}[./]\d{1,2}[./]\d{2,4}\b'
    """Regex pattern for matching birthday dates."""

    BIRTHDAY_STRICT_PATTERN = r'\d{2}\.\d{2}\.\d{4}'
    """Strict regex pattern for DD.MM.YYYY format."""

    # Tag pattern
    TAG_PATTERN = r'#[\w-]+'
    """Regex pattern for matching hashtags."""

    # UUID pattern
    UUID_PATTERN = r'\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b'
    """Regex pattern for matching UUIDs."""

    # Name patterns
    NAME_POSSESSIVE_PATTERN = r'\b([A-Z][a-z]+)(?=\'s\b)'
    """Regex pattern for extracting possessive names (e.g., John's)."""

    NAME_FULL_PATTERN = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})\b'
    """Regex pattern for extracting full names (2-3 words capitalized)."""

    # Address patterns
    ADDRESS_CITY_PATTERN = r',\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)$'
    """Regex pattern for extracting city from address."""

    # Validation patterns
    VALIDATION_EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    """Strict email validation pattern."""

    VALIDATION_NAME_PATTERN = r'^[a-zA-ZÀ-ÿ\s\-\']+$'
    """Name validation pattern (allows letters, spaces, hyphens, apostrophes, accented chars)."""

    VALIDATION_ADDRESS_PATTERN = r'^(?=.*[a-zA-Z0-9])[a-zA-Z0-9\s.,/\-#]+$'
    """Address validation pattern."""

    TAG_INVALID_CHAR_PATTERN = r'[^\w#]'
    """Pattern for removing invalid characters from tags."""

    # Quoted text patterns for note extraction
    QUOTED_PATTERNS = [
        r'"([^"]+)"',
        r"'([^']+)'",
        r'«([^»]+)»',
        r'„([^"]+)"'
    ]
    """Patterns for extracting quoted text as note content."""


# =============================================================================
# Date Format Configuration
# =============================================================================

class DateFormatConfig:

    # Primary date format
    PRIMARY_DATE_FORMAT = "%d.%m.%Y"
    """Primary date format used throughout the application (DD.MM.YYYY)."""

    # Minimum year for birthday validation
    MIN_BIRTHDAY_YEAR = 1900
    """Minimum allowed year for birthday dates."""


# =============================================================================
# Phone Configuration
# =============================================================================

class PhoneConfig:

    # Exact phone length for validation
    EXACT_PHONE_LENGTH = 10
    """Exact expected length for phone numbers (digits only)."""
