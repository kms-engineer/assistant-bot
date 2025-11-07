
class EntityConfig:

    # Entity labels (IOB2 format)
    ENTITY_LABELS = [
        "O", "B-NAME", "I-NAME", "B-PHONE", "I-PHONE", "B-OLD_PHONE", "I-OLD_PHONE",
        "B-NEW_PHONE", "I-NEW_PHONE", "B-EMAIL", "I-EMAIL",
        "B-ADDRESS", "I-ADDRESS", "B-BIRTHDAY", "I-BIRTHDAY", "B-TAG", "I-TAG",
        "B-NOTE_TEXT", "I-NOTE_TEXT", "B-ID", "I-ID", "B-DAYS", "I-DAYS"
    ]
    """Complete list of entity labels in IOB2 format."""

    # Entity field preferences (regex vs NER)
    REGEX_PREFERRED_FIELDS = {'phone', 'old_phone', 'new_phone', 'email', 'birthday', 'tag', 'id'}
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

    # Excluded words for name extraction (command words that should not be treated as names)
    NAME_EXCLUDED_WORDS = {
        'Add', 'Edit', 'Delete', 'Remove', 'Show', 'List', 'Create', 'New', 'Update',
        'Change', 'Find', 'Search', 'Contact', 'Note', 'Birthday', 'Tag', 'Email',
        'Phone', 'Address', 'Help', 'Exit', 'From', 'To', 'With', 'For', 'And'
    }
    """Command words that should be excluded from name extraction."""

    # Heuristic stop words for name extraction (comprehensive list)
    HEURISTIC_STOP_WORDS = {
        # Commands
        'Add', 'Create', 'Save', 'Update', 'Change', 'Edit', 'Delete', 'Remove',
        'Set', 'Get', 'Show', 'List', 'Search', 'Find', 'Display', 'New',
        # Entities
        'Person', 'Contact', 'Entry', 'Record', 'User', 'Client', 'Member',
        'Phone', 'Email', 'Address', 'Birthday', 'Note', 'Tag', 'Info',
        # Months
        'January', 'February', 'March', 'April', 'May', 'June', 'July',
        'August', 'September', 'October', 'November', 'December',
        # Days of week
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
        # Modal/polite words
        'Please', 'Can', 'Could', 'Would', 'Should', 'Will', 'May', 'Might',
        # Address components
        'Suite', 'Apt', 'Apartment', 'Unit', 'Building', 'Floor', 'Room'
    }
    """Comprehensive stop words for heuristic name extraction."""

    # Command words to filter from name extraction (lowercase for case-insensitive matching)
    COMMAND_WORDS = {
        # Action verbs
        'show', 'display', 'get', 'view', 'find', 'search', 'lookup', 'locate',
        'add', 'create', 'new', 'edit', 'update', 'change', 'modify',
        'delete', 'remove', 'erase', 'list', 'all',
        # Entity types
        'contact', 'person', 'note', 'birthday', 'phone', 'email', 'address',
        'tag', 'info', 'information', 'details',
        # Common words
        'the', 'a', 'an', 'for', 'from', 'to', 'with', 'about', 'of'
    }
    """Command words that should not be part of extracted entity values (lowercase)."""
