
INTENT_REQUIREMENTS = {
    "add_contact": {
        "required": ["name", "phone"],
        "optional": ["email", "address", "birthday"]
    },
    "add_phone": {
        "required": ["name", "phone"],
        "optional": []
    },
    "edit_phone": {
        "required": ["name", "old_phone", "new_phone"],
        "optional": []
    },
    "remove_phone": {
        "required": ["name", "phone"],
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
        "required": [],
        "optional": ["name", "phone", "email"]
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
        "required": ["note_text"],
        "optional": ["tag"]
    },
    "edit_note": {
        "required": ["id", "note_text"],
        "optional": []
    },
    "remove_note": {
        "required": ["id"],
        "optional": []
    },
    "show_notes": {
        "required": [],
        "optional": []
    },
    "show_note": {
        "required": ["id"],
        "optional": []
    },
    "add_note_tag": {
        "required": ["id", "tag"],
        "optional": []
    },
    "remove_note_tag": {
        "required": ["id", "tag"],
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
    },
    "show_phone": {
        "required": ["name"],
        "optional": []
    },
    "add_email": {
        "required": ["name", "email"],
        "optional": []
    },
    "remove_email": {
        "required": ["name"],
        "optional": []
    },
    "add_address": {
        "required": ["name", "address"],
        "optional": []
    },
    "remove_address": {
        "required": ["name"],
        "optional": []
    },
    "show_birthday": {
        "required": ["name"],
        "optional": []
    },
    "clear": {
        "required": [],
        "optional": []
    },
    "save": {
        "required": ["filename"],
        "optional": []
    },
    "load": {
        "required": ["filename"],
        "optional": []
    },
    "list_note_tags": {
        "required": [],
        "optional": []
    },
}
