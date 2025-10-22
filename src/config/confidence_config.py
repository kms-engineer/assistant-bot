
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
