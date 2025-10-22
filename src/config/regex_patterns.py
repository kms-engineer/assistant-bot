
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
