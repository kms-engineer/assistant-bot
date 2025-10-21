from typing import Dict


class IntentValidator:

    # Define required entities per intent
    REQUIRED_ENTITIES = {
        'add_contact': ['name'],  # At minimum, need a name
        'edit_phone': ['name'],  # Need name to identify contact
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

    @staticmethod
    def validate_for_intent(entities: Dict, intent: str) -> Dict:
        required = IntentValidator.REQUIRED_ENTITIES.get(intent, [])
        missing = [field for field in required if field not in entities or not entities[field]]

        return {
            'valid': len(missing) == 0,
            'missing': missing,
            'required': required
        }
