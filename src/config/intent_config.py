
class IntentConfig:

    # All supported intent labels (26 unique intents)
    INTENT_LABELS = [
        "add_contact", "edit_phone", "edit_email", "edit_address", "delete_contact",
        "list_all_contacts", "search_contacts", "add_birthday", "list_birthdays",
        "add_note", "edit_note", "remove_note", "show_notes", "add_note_tag",
        "remove_note_tag", "search_notes_text", "search_notes_by_tag",
        "help", "exit", "hello",
        "show_phone", "add_email", "remove_email", "add_address", "remove_address",
        "show_birthday"
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
        'remove_note': 'delete-note',
        'delete_note': 'delete-note',  # Alias for remove_note
        'show_notes': 'show-notes',
        'add_note_tag': 'add-tag',
        'remove_note_tag': 'remove-tag',
        'search_notes_text': 'search-notes',
        'search_notes_by_tag': 'search-by-tag',
        'hello': 'hello',
        'help': 'help',
        'exit': 'exit',
        'show_phone': 'phone',
        'add_email': 'add-email',
        'remove_email': 'remove-email',
        'add_address': 'add-address',
        'remove_address': 'remove-address',
        'show_birthday': 'show-birthday'
    }
    """Maps intent labels to corresponding command names."""

    # Import large data structures from separate modules
    from .keyword_map import KEYWORD_MAP
    from .pipeline_definitions import PIPELINE_DEFINITIONS
    from .intent_requirements import INTENT_REQUIREMENTS

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
