from typing import Dict


class IntentValidator:

    # Define required entities per intent
    REQUIRED_ENTITIES = {
        'add_contact': ['name', 'phone'],  # Need name and phone for add
        'edit_phone': ['name', 'phone'],  # Need name and new phone
        'edit_email': ['name', 'email'],
        'edit_address': ['name', 'address'],
        'delete_contact': ['name'],
        'search_contacts': [],  # Can search without specific entity
        'add_birthday': ['name', 'birthday'],
        'add_note': ['note_text'],
        'edit_note': ['id', 'note_text'],  # Need ID to identify note
        'delete_note': ['id'],
        'add_note_tag': ['id', 'tag'],
        'remove_note_tag': ['id', 'tag'],
        'search_notes_text': [],
        'search_notes_by_tag': ['tag'],
    }

    # Define optional entities that can trigger pipeline execution
    OPTIONAL_ENTITIES = {
        'add_contact': ['email', 'address', 'birthday'],
        'edit_phone': ['email', 'address', 'birthday'],
        'add_note': ['tag'],
        'search_contacts': ['name', 'phone', 'email'],
    }

    @staticmethod
    def validate_for_intent(entities: Dict, intent: str) -> Dict:
        required = IntentValidator.REQUIRED_ENTITIES.get(intent, [])
        optional = IntentValidator.OPTIONAL_ENTITIES.get(intent, [])
        missing = [field for field in required if field not in entities or not entities[field]]

        # Count how many optional entities are present
        optional_present = [field for field in optional if field in entities and entities[field]]

        return {
            'valid': len(missing) == 0,
            'missing': missing,
            'required': required,
            'optional': optional,
            'optional_present': optional_present,
            'has_optional': len(optional_present) > 0
        }
