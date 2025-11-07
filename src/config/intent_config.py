
class IntentConfig:

    # NOTE: This list is for reference only. The actual intent labels are loaded
    # from the trained model's label_map.json file at runtime.
    # All supported intent labels (32 unique intents)
    INTENT_LABELS = [
        "add_contact", "edit_phone", "edit_email", "edit_address", "delete_contact",
        "list_all_contacts", "search_contacts", "add_birthday", "list_birthdays",
        "add_note", "edit_note", "remove_note", "show_notes", "show_note", "add_note_tag",
        "remove_note_tag", "search_notes_text", "search_notes_by_tag",
        "help", "exit", "hello",
        "show_phone", "add_email", "remove_email", "add_address", "remove_address",
        "show_birthday", "clear", "save", "load", "remove_phone",
        "list_note_tags"
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
        'show_note': 'show-note',
        'add_note_tag': 'add-tag',
        'remove_note_tag': 'remove-tag',
        'search_notes_text': 'search-notes',
        'search_notes_by_tag': 'search-notes-by-tag',
        'hello': 'hello',
        'help': 'help',
        'exit': 'exit',
        'show_phone': 'phone',
        'add_email': 'add-email',
        'remove_email': 'remove-email',
        'add_address': 'add-address',
        'remove_address': 'remove-address',
        'show_birthday': 'show-birthday',
        'clear': 'clear',
        'save': 'save',
        'load': 'load',
        'remove_phone': 'remove-phone',
        'list_note_tags': 'list-tags'
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

    # NLP command examples for user help
    NLP_COMMAND_EXAMPLES = [
        # Contact management
        "add a contact",
        "add contact with phone",
        "add contact with email and address",
        "change phone number",
        "delete a contact",
        "remove a contact",
        "show phone for contact",
        "show all contacts",
        "list all contacts",

        # Birthday commands
        "add birthday",
        "add birthday for contact",
        "show birthday",
        "show upcoming birthdays",
        "show birthdays for next week",

        # Email commands
        "add email",
        "add email to contact",
        "edit email",
        "change email",
        "remove email",
        "delete email",

        # Address commands
        "add address",
        "add address to contact",
        "edit address",
        "change address",
        "remove address",
        "delete address",

        # Search and find
        "search contacts",
        "search for contact",
        "find contact",
        "find by name",

        # Note commands
        "add a note",
        "create a note",
        "show my notes",
        "show all notes",
        "show note",
        "show note with id",
        "display note",
        "view note",
        "edit a note",
        "update a note",
        "delete a note",
        "remove a note",

        # Note tag commands
        "add tag to note",
        "add tag",
        "remove tag from note",
        "remove tag",
        "search notes",
        "search notes by text",
        "search notes by tag",
        "find notes with tag",

        # General commands
        "hello",
        "help",
        "save",
        "load",
        "exit",
        "close",
    ]
    """Example natural language commands for user reference."""
