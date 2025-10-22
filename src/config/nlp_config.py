
class NLPConfig:
    """Natural Language Processing configuration parameters."""

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
