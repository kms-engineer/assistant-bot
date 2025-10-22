
INTENT_REQUIREMENTS = {
    "add_contact": {
        "required": ["name"],
        "optional": ["phone", "email", "address", "birthday"]
    },
    "edit_phone": {
        "required": ["name", "old_phone", "new_phone"],
        "optional": []
    },
    "edit_email": {
        "required": ["name", "email"],
        "optional": []
    },
    "edit_address": {
        "required": ["name", "address"],
        "optional": []
    },
    "delete_contact": {
        "required": ["name"],
        "optional": []
    },
    "list_all_contacts": {
        "required": [],
        "optional": []
    },
    "search_contacts": {
        "required": ["name"],
        "optional": []
    },
    "add_birthday": {
        "required": ["name", "birthday"],
        "optional": []
    },
    "list_birthdays": {
        "required": [],
        "optional": ["days"]
    },
    "add_note": {
        "required": ["name", "note_text"],
        "optional": []
    },
    "edit_note": {
        "required": ["name", "id", "note_text"],
        "optional": []
    },
    "delete_note": {
        "required": ["name", "id"],
        "optional": []
    },
    "show_notes": {
        "required": ["name"],
        "optional": []
    },
    "add_note_tag": {
        "required": ["name", "id", "tag"],
        "optional": []
    },
    "remove_note_tag": {
        "required": ["name", "id", "tag"],
        "optional": []
    },
    "search_notes_text": {
        "required": ["note_text"],
        "optional": ["name"]
    },
    "search_notes_by_tag": {
        "required": ["tag"],
        "optional": ["name"]
    },
    "hello": {
        "required": [],
        "optional": []
    },
    "help": {
        "required": [],
        "optional": []
    },
    "exit": {
        "required": [],
        "optional": []
    }
}
