
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

    # Date parsing patterns for normalizers
    BIRTHDAY_PARSE_DD_MM_YYYY = r'(\d{1,2})[./](\d{1,2})[./](\d{4})'
    """Pattern for DD.MM.YYYY or DD/MM/YYYY format."""

    BIRTHDAY_PARSE_YYYY_MM_DD = r'(\d{4})-(\d{1,2})-(\d{1,2})'
    """Pattern for YYYY-MM-DD format."""

    BIRTHDAY_PARSE_MM_DD_YYYY = r'(\d{1,2})/(\d{1,2})/(\d{4})'
    """Pattern for MM/DD/YYYY (US) format."""

    # Date patterns for library extractor (more formats)
    DATE_PATTERN_SLASH_DOT = r'\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b'
    """Date pattern with slashes or dots (MM/DD/YYYY, DD-MM-YYYY, etc)."""

    DATE_PATTERN_ISO = r'\b\d{4}[./-]\d{1,2}[./-]\d{1,2}\b'
    """Date pattern in ISO format (YYYY-MM-DD)."""

    DATE_PATTERN_MONTH_NAME = r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b'
    """Date pattern with month names (Jan 15, 2020 or January 15 2020)."""

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

    # Phone patterns (advanced)
    PHONE_PATTERN_ADVANCED = (
        r'(?:\+?1[-.\s]?)?'  # Optional country code
        r'(?:\(?\d{3}\)?[-.\s]?)'  # Area code (with optional parens)
        r'\d{3}[-.\s]?\d{4}(?!\d)'  # Main number (negative lookahead to avoid over-matching)
    )
    """Advanced phone pattern with country code and area code support."""

    # Birthday patterns (combined)
    BIRTHDAY_PATTERN_COMBINED = (
        r'\b(?:'
        r'\d{1,2}[./-]\d{1,2}[./-]\d{2,4}|'  # DD.MM.YYYY, DD/MM/YYYY, etc.
        r'\d{4}[./-]\d{1,2}[./-]\d{1,2}|'  # YYYY-MM-DD
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}|'  # Month DD, YYYY
        r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}'  # DD Month YYYY
        r')\b'
    )
    """Combined birthday pattern supporting multiple formats."""

    # Quoted text patterns for note extraction
    QUOTED_PATTERNS = [
        r'"([^"]+)"',
        r"'([^']+)'",
        r'«([^»]+)»',
        r'„([^"]+)"'
    ]
    """Patterns for extracting quoted text as note content."""

    QUOTED_PATTERNS_EXTENDED = [
        r'["\']([^"\']{2,})["\']',  # Standard quotes
        r'[\u2018\u2019]([^\u2018\u2019]{2,})[\u2018\u2019]',  # Smart single quotes
        r'[\u201C\u201D]([^\u201C\u201D]{2,})[\u201C\u201D]',  # Smart double quotes
    ]
    """Extended patterns for extracting quoted text including smart quotes."""

    # Note command patterns
    NOTE_COMMAND_PATTERNS = [
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
    """Patterns for removing note command prefixes."""

    # Cleanup patterns
    WHITESPACE_NORMALIZE_PATTERN = r'\s+'
    """Pattern for normalizing multiple spaces."""

    LEADING_PUNCTUATION_PATTERN = r'^\s*[:;,.\\-]\s*'
    """Pattern for removing leading punctuation."""

    TRAILING_PUNCTUATION_PATTERN = r'\s*[:;,.\\-]\s*$'
    """Pattern for removing trailing punctuation."""

    # Address patterns (heuristic)
    ADDRESS_CITY_STATE_ZIP_PATTERN = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s*({state_pattern})\s+(\d{{5}}(?:-\d{{4}})?)\b'
    """Pattern for City, State ZIP format (state_pattern placeholder will be replaced)."""

    ADDRESS_STREET_PATTERN = r'\b\d+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:{street_suffixes})\b'
    """Pattern for street addresses (street_suffixes placeholder will be replaced)."""

    # Template parser specific patterns
    TEMPLATE_PHONE_PATTERNS = [
        r'\+?1?\s*\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})',  # US format
        r'\+?(\d{1,3})[\s.-]?\(?(\d{2,4})\)?[\s.-]?(\d{3,4})[\s.-]?(\d{4})',  # International
        r'\b(\d{10})\b',  # 10 digits
        r'\b(\d{3})[\s.-]?(\d{3})[\s.-]?(\d{4})\b',  # Variations
        r'\b(\d{3})[\s.-]?(\d{4})\b',  # Short format 555-9999
        r'\b(\d{7,})\b'  # Any sequence of 7+ digits as fallback
    ]
    """Template parser phone patterns (list of patterns to try in order)."""

    TEMPLATE_ID_PATTERNS = [
        r'note\s+(?:id\s+)?(\d+)',
        r'id\s+(\d+)',
        r'#(\d+)'
    ]
    """Template parser ID patterns for notes."""

    TEMPLATE_ADDRESS_STREET_FULL = r'\d+\s+[A-Z][a-z]+\s+(Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)'
    """Template parser street address pattern with full suffixes."""

    TEMPLATE_ADDRESS_FROM_PATTERN = r'from\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:,\s*[A-Z][a-z]+)?)'
    """Template parser address pattern for 'from City, Country' format."""

    TEMPLATE_NOTE_TEXT_PATTERNS = [
        r'(?:add|create|new)\s+note\s+["\']?(.+?)["\']?$',  # add/create note <text>
        r'(?:edit|update)\s+note\s+\d+\s+(.+)$',  # edit note 5 <text>
        r'note:\s*(.+)$',  # note: <text>
        r'note\s+(?:id\s+)?\d+\s+(.+)$'  # note 5 <text> or note id 5 <text>
    ]
    """Template parser note text extraction patterns."""

    # Post-processing patterns
    POST_PHONE_FROM_TO_PATTERN = r'(?:from\s+)?(\d[\d\s\-\.]+?)\s+(?:to|->)\s+(\d[\d\s\-\.]+)'
    """Pattern for extracting old and new phone: 'from 123 to 456' or '123 to 456'."""

    POST_PHONE_ALL_PATTERN = r'\d{10,}'
    """Pattern for extracting all phone numbers (10+ digits)."""

    POST_DAYS_NUMBER_PATTERN = r'(\d+)'
    """Pattern for extracting number from days field."""

    POST_DAYS_IN_ADDRESS_PATTERN = r'^\d+\s*days?$'
    """Pattern for detecting days mistakenly extracted as address."""
