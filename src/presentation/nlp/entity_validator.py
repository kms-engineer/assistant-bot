from typing import Dict, List
from src.config import IntentConfig


class EntityValidator:

    # Get intent requirements from config
    INTENT_REQUIREMENTS_BASE = IntentConfig.INTENT_REQUIREMENTS

    # Extended intent requirements with additional metadata
    INTENT_REQUIREMENTS = {
        "add_contact": {
            "required": ["name", "phone"],
            "optional": ["email", "address", "birthday"],
            "optional_min": 0,  # Changed from 2 to 0 - at least name+phone is enough
            "description": "Add new contact with name+phone (email, address, birthday are optional)"
        },
        "edit_phone": {
            "required": ["name", "phone"],
            "optional": [],
            "optional_min": 0,
            "description": "Change phone number for contact"
        },
        "edit_email": {
            "required": ["name", "email"],
            "optional": [],
            "optional_min": 0,
            "description": "Update email address for contact"
        },
        "edit_address": {
            "required": ["name", "address"],
            "optional": [],
            "optional_min": 0,
            "description": "Update address for contact"
        },
        "delete_contact": {
            "required": ["name"],
            "optional": [],
            "optional_min": 0,
            "description": "Delete contact by name"
        },
        "search_contacts": {
            "required": ["query"],
            "optional": [],
            "optional_min": 0,
            "description": "Search contacts by name or other fields"
        },
        "add_birthday": {
            "required": ["name", "birthday"],
            "optional": [],
            "optional_min": 0,
            "description": "Add or update birthday for contact"
        },
        "list_birthdays": {
            "required": [],
            "optional": ["days", "weeks", "months"],
            "optional_min": 0,
            "description": "List upcoming birthdays"
        },
        "add_note": {
            "required": ["note_text"],
            "optional": ["tag"],
            "optional_min": 0,
            "description": "Create new note"
        },
        "edit_note": {
            "required": ["id", "note_text"],
            "optional": [],
            "optional_min": 0,
            "description": "Edit existing note"
        },
        "remove_note": {
            "required": ["id"],
            "optional": [],
            "optional_min": 0,
            "description": "Remove note by ID"
        },
        "show_notes": {
            "required": [],
            "optional": [],
            "optional_min": 0,
            "description": "Show all notes"
        },
        "add_note_tag": {
            "required": ["id", "tag"],
            "optional": [],
            "optional_min": 0,
            "description": "Add tag to note"
        },
        "remove_note_tag": {
            "required": ["id", "tag"],
            "optional": [],
            "optional_min": 0,
            "description": "Remove tag from note"
        },
        "search_notes_text": {
            "required": ["note_text"],
            "optional": [],
            "optional_min": 0,
            "description": "Search notes by text content"
        },
        "search_notes_by_tag": {
            "required": ["tag"],
            "optional": [],
            "optional_min": 0,
            "description": "Search notes by tag"
        },
        "list_all_contacts": {
            "required": [],
            "optional": [],
            "optional_min": 0,
            "description": "List all contacts"
        },
        "hello": {
            "required": [],
            "optional": [],
            "optional_min": 0,
            "description": "Hello"
        },
        "help": {
            "required": [],
            "optional": [],
            "optional_min": 0,
            "description": "Show help information"
        },
        "exit": {
            "required": [],
            "optional": [],
            "optional_min": 0,
            "description": "Exit the application"
        },
        "show_phone": {
            "required": ["name"],
            "optional": [],
            "optional_min": 0,
            "description": "Show phone number for contact"
        },
        "add_email": {
            "required": ["name", "email"],
            "optional": [],
            "optional_min": 0,
            "description": "Add email to contact"
        },
        "remove_email": {
            "required": ["name"],
            "optional": [],
            "optional_min": 0,
            "description": "Remove email from contact"
        },
        "add_address": {
            "required": ["name", "address"],
            "optional": [],
            "optional_min": 0,
            "description": "Add address to contact"
        },
        "remove_address": {
            "required": ["name"],
            "optional": [],
            "optional_min": 0,
            "description": "Remove address from contact"
        },
        "show_birthday": {
            "required": ["name"],
            "optional": [],
            "optional_min": 0,
            "description": "Show birthday for contact"
        },
    }

    def __init__(self):
        pass

    def validate(self, entities: Dict[str, str], intent: str) -> Dict:
        if intent not in self.INTENT_REQUIREMENTS:
            # Unknown intent, no validation
            return {
                "valid": True,
                "missing_required": [],
                "optional_count": 0,
                "optional_needed": 0,
                "needs_ner": False,
                "reason": f"Unknown intent: {intent}"
            }

        requirements = self.INTENT_REQUIREMENTS[intent]
        required_fields = requirements["required"]
        optional_fields = requirements["optional"]
        optional_min = requirements["optional_min"]

        # Normalize entity keys to lowercase for matching
        entities_lower = {k.lower(): v for k, v in entities.items() if v}

        # Check required fields
        missing_required = []
        for field in required_fields:
            if field.lower() not in entities_lower:
                missing_required.append(field)

        # Count optional fields
        optional_count = 0
        for field in optional_fields:
            if field.lower() in entities_lower:
                optional_count += 1

        # Determine if NER model is needed
        needs_ner = False
        reason = ""

        if missing_required:
            needs_ner = True
            reason = f"Missing required fields: {', '.join(missing_required)}"
        elif optional_count < optional_min:
            needs_ner = True
            reason = f"Insufficient optional fields: {optional_count}/{len(optional_fields)} found, need at least {optional_min}"

        # Overall validation
        valid = not missing_required and (optional_count >= optional_min)

        return {
            "valid": valid,
            "missing_required": missing_required,
            "optional_count": optional_count,
            "optional_needed": optional_min,
            "optional_available": len(optional_fields),
            "needs_ner": needs_ner,
            "reason": reason if needs_ner else "All requirements met"
        }

    def should_use_ner(self, validation_result: Dict) -> bool:
        return validation_result.get("needs_ner", False)

    def get_intent_requirements(self, intent: str) -> Dict:
        return self.INTENT_REQUIREMENTS.get(intent, {})

    def get_all_intents(self) -> List[str]:
        return list(self.INTENT_REQUIREMENTS.keys())
