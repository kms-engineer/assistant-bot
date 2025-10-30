
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
    PHONE_MIN_DIGITS = 8
    """Minimum number of digits in a phone number."""

    PHONE_MAX_DIGITS = 15
    """Maximum number of digits in a phone number."""

    # Error messages - Name
    NAME_ERROR_EMPTY = "Name cannot be empty or whitespace"
    NAME_ERROR_TOO_SHORT = f"Name must be at least {NAME_MIN_LENGTH} characters long"
    NAME_ERROR_TOO_LONG = f"Name must be at most {NAME_MAX_LENGTH} characters long"
    NAME_ERROR_INVALID_CHARS = "Name can only contain letters, spaces, and hyphens"

    # Error messages - Email
    EMAIL_ERROR_EMPTY = "Email cannot be empty or whitespace"
    EMAIL_ERROR_INVALID_FORMAT = "Email must be a valid email address (e.g., user@example.com)"

    # Error messages - Phone
    PHONE_ERROR_NOT_STRING = "Phone number must be string value"
    PHONE_ERROR_INVALID_LENGTH = f"Phone number must contain between {PHONE_MIN_DIGITS} and {PHONE_MAX_DIGITS} digits"
    PHONE_ERROR_INVALID_FORMAT = "Phone number must start with + or a digit and contain only digits"

    # Error messages - Birthday
    BIRTHDAY_ERROR_NOT_STRING = "Birthday must be a string"
    BIRTHDAY_ERROR_EMPTY = "Birthday cannot be empty or whitespace"
    BIRTHDAY_ERROR_INVALID_FORMAT = "Birthday contain invalid date format. Use DD.MM.YYYY"
    BIRTHDAY_ERROR_FUTURE_DATE = "Birthday cannot be in future"
    BIRTHDAY_ERROR_INVALID_YEAR = "Birthday contain invalid year"
    BIRTHDAY_ERROR_INVALID_MONTH = "Birthday contain invalid month"
    BIRTHDAY_ERROR_INVALID_DATE = "Birthday contain invalid date"

    # Error messages - Tag
    TAG_ERROR_NOT_STRING = "Tag must be a string"
    TAG_ERROR_EMPTY = "Tag cannot be empty"
    TAG_ERROR_TOO_LONG = f"Tag too long (max {TAG_MAX_LENGTH} characters)"

    # Error messages - Address
    ADDRESS_ERROR_EMPTY = "Address cannot be empty or whitespace"
    ADDRESS_ERROR_TOO_SHORT = f"Address must be at least {ADDRESS_MIN_LENGTH} characters long"
    ADDRESS_ERROR_TOO_LONG = f"Address must be at most {ADDRESS_MAX_LENGTH} characters long"
    ADDRESS_ERROR_INVALID_FORMAT = "Address must contain valid characters"

    # Error messages - Note Text
    NOTE_ERROR_NOT_STRING = "Note text must be a string"
    NOTE_ERROR_EMPTY = "Note text cannot be empty or whitespace"
    NOTE_ERROR_TOO_SHORT = "Note text must be at least 2 characters long"
