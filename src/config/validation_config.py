
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
