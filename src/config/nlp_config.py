from typing import Dict, Set, List


class NLPConfig:

    # ============================================================================
    # CONFIDENCE THRESHOLDS
    # ============================================================================

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

    # Hybrid intent selection thresholds
    ML_LOW_CONFIDENCE_THRESHOLD = 0.7
    """Below this, consider keyword match as alternative."""

    KEYWORD_HIGH_CONFIDENCE_THRESHOLD = 0.8
    """Above this, prefer keyword match over ML."""

    # Default region for phone number parsing
    DEFAULT_REGION = "US"
    """Default region code for phone number validation and formatting."""

    # ============================================================================
    # ACTION CATEGORIES
    # ============================================================================

    # Category keywords for action type detection
    CATEGORY_KEYWORDS: Dict[str, Set[str]] = {
        "add": {"add", "create", "new", "attach", "set", "insert", "save", "register"},
        "edit": {
            "edit",
            "update",
            "change",
            "modify",
            "replace",
            "fix",
            "correct",
            "adjust",
        },
        "remove": {"remove", "delete", "clear", "erase", "drop", "unset", "destroy"},
        "search": {
            "search",
            "find",
            "lookup",
            "locate",
            "get",
            "show me",
            "where",
            "which",
        },
        "show": {"show", "list", "display", "view", "all", "print", "output", "see"},
    }

    # Mapping from category to intent list
    CATEGORY_TO_INTENTS: Dict[str, List[str]] = {
        "add": [
            "add_contact",
            "add_email",
            "add_address",
            "add_birthday",
            "add_note",
            "add_note_tag",
        ],
        "edit": ["edit_phone", "edit_email", "edit_address", "edit_note"],
        "remove": [
            "remove_email",
            "remove_address",
            "remove_phone",
            "remove_birthday",
            "remove_note",
            "remove_note_tag",
            "delete_contact",
        ],
        "search": ["search_contacts", "search_notes_text", "search_notes_by_tag"],
        "show": [
            "show_phone",
            "show_birthday",
            "show_notes",
            "show_note",
            "list_all_contacts",
            "list_birthdays",
            "list_note_tags",
        ],
    }

    # ============================================================================
    # KEYWORD INTENT PATTERNS
    # ============================================================================

    # Intent patterns for keyword-based matching
    # Each pattern has: required (all must match), optional (boost confidence), confidence
    INTENT_PATTERNS: Dict[str, List[Dict]] = {
        "add_contact": [
            {
                "required": [["add", "create", "new"]],
                "optional": ["contact", "person", "name", "phone"],
                "confidence": 0.85,
            },
        ],
        "edit_phone": [
            {
                "required": [
                    ["change", "edit", "update", "modify"],
                    ["phone", "number"],
                ],
                "optional": [],
                "confidence": 0.90,
            },
        ],
        "delete_contact": [
            {
                "required": [["delete", "remove"], ["contact"]],
                "optional": ["person", "name"],
                "confidence": 0.90,
            },
        ],
        "search_contacts": [
            {
                "required": [
                    ["search", "find", "lookup", "locate"],
                    ["contact", "person"],
                ],
                "optional": ["name", "phone", "email"],
                "confidence": 0.90,
            },
            {
                "required": [["show", "get", "display", "view"], ["contact", "person"]],
                "optional": ["info", "information", "details", "for"],
                "confidence": 0.85,
            },
            {
                "required": [["search", "find", "lookup", "locate"], ["for"]],
                "optional": ["contact", "person"],
                "confidence": 0.95,
            },
            {
                "required": [["search", "find", "lookup", "locate"]],
                "optional": ["name", "phone", "email"],
                "confidence": 0.80,
            },
        ],
        "show_phone": [
            {
                "required": [["show", "display", "get"], ["phone", "number"]],
                "optional": ["contact", "for"],
                "confidence": 0.85,
            },
            {
                "required": [["what", "whats"], ["phone", "number"]],
                "optional": [],
                "confidence": 0.85,
            },
        ],
        "list_all_contacts": [
            {
                "required": [["all"], ["contacts", "people"]],
                "optional": ["show", "list", "display"],
                "confidence": 0.95,
            },
            {
                "required": [["show", "list", "display"], ["contacts", "people"]],
                "optional": ["all"],
                "confidence": 0.90,
            },
            {"required": [["contacts", "people"]], "optional": [], "confidence": 0.80},
        ],
        "add_birthday": [
            {
                "required": [["add", "set"], ["birthday", "birthdate"]],
                "optional": ["for", "contact"],
                "confidence": 0.90,
            },
        ],
        "remove_birthday": [
            {
                "required": [
                    ["remove", "delete", "clear", "erase"],
                    ["birthday", "birthdate"],
                ],
                "optional": ["for", "from"],
                "confidence": 0.90,
            },
        ],
        "show_birthday": [
            {
                "required": [["show", "get", "whats"], ["birthday", "birthdate"]],
                "optional": ["for"],
                "confidence": 0.85,
            },
        ],
        "add_email": [
            {
                "required": [["add", "set"], ["email"]],
                "optional": ["address", "for", "contact"],
                "confidence": 0.90,
            },
        ],
        "remove_email": [
            {
                "required": [["remove", "delete"], ["email"]],
                "optional": ["address", "from"],
                "confidence": 0.90,
            },
        ],
        "add_address": [
            {
                "required": [["add", "set"], ["address"]],
                "optional": ["for", "contact"],
                "confidence": 0.90,
            },
        ],
        "edit_address": [
            {
                "required": [["change", "edit", "update", "modify"], ["address"]],
                "optional": ["for", "to"],
                "confidence": 0.90,
            },
        ],
        "remove_address": [
            {
                "required": [["remove", "delete"], ["address"]],
                "optional": ["from"],
                "confidence": 0.90,
            },
        ],
        "remove_phone": [
            {
                "required": [["remove", "delete"], ["phone", "number"]],
                "optional": ["from"],
                "confidence": 0.97,
            },
        ],
        "add_note": [
            {
                "required": [["add", "create", "new"], ["note"]],
                "optional": [],
                "confidence": 0.85,
            },
        ],
        "show_notes": [
            {
                "required": [["show", "list", "display"], ["notes"]],
                "optional": ["all", "my"],
                "confidence": 0.90,
            },
            {"required": [["notes"]], "optional": ["all", "my"], "confidence": 0.75},
        ],
        "show_note": [
            {
                "required": [["show", "display", "get", "view"], ["note"]],
                "optional": ["id"],
                "confidence": 0.85,
            },
        ],
        "search_notes_text": [
            {
                "required": [["search", "find"], ["notes", "note"]],
                "optional": ["for", "about", "with", "text"],
                "confidence": 0.85,
            },
        ],
        "search_notes_by_tag": [
            {
                "required": [["tag", "tagged", "tags"]],
                "optional": ["notes", "note", "with", "by"],
                "confidence": 0.90,
            },
            {
                "required": [["search", "find"], ["tag"]],
                "optional": ["notes", "note", "by"],
                "confidence": 0.85,
            },
        ],
        "help": [
            {
                "required": [["help", "commands", "what can you do"]],
                "optional": [],
                "confidence": 0.95,
            },
        ],
        "hello": [
            {
                "required": [["hello", "hi", "hey", "greetings"]],
                "optional": [],
                "confidence": 0.95,
            },
        ],
    }
