
KEYWORD_MAP = {
    "add_contact": [
        "add contact", "new contact", "create contact", "save contact",
        "add person", "new person", "create person", "save person",
        "store contact", "store person", "add to contacts", "save to contacts",
        "add to address book", "save in contacts", "save new person"
    ],
    "edit_phone": [
        "change phone", "edit phone", "update phone", "modify phone",
        "replace phone", "new phone", "phone to", "phone from",
        "set phone", "update number", "change number", "modify number",
        "replace number", "phone number to"
    ],
    "edit_email": [
        "change email", "edit email", "update email", "modify email",
        "set email", "replace email", "email to", "new email",
        "email address to", "replace email with"
    ],
    "edit_address": [
        "change address", "edit address", "update address", "modify address",
        "set address", "replace address", "address to", "new address",
        "address with"
    ],
    "delete_contact": [
        "delete contact", "remove contact", "erase contact",
        "delete person", "remove person", "erase person",
        "remove from contacts", "delete from contacts",
        "remove from address book", "delete from address book",
        "erase from contacts"
    ],
    "list_all_contacts": [
        "all contacts", "show all", "list all", "display all",
        "show contacts", "list contacts", "display contacts",
        "show everyone", "list everyone", "everyone in", "all in"
    ],
    "search_contacts": [
        "find contact", "search contact", "look up", "look for",
        "find person", "search person", "search for", "find in",
        "search in contacts", "find in contacts", "find in address book",
        "show contact", "show info", "contact info", "get contact",
        "view contact", "display contact"
    ],
    "add_birthday": [
        "add birthday", "set birthday", "save birthday",
        "birthday for", "born on", "birth date", "birthday to",
        "birthday as", "record birthday", "was born"
    ],
    "list_birthdays": [
        "show birthday", "list birthday", "upcoming birthday",
        "birthdays for", "birthdays in", "who has birthday",
        "birthdays next", "birthday this", "birthdays coming"
    ],
    "add_note": [
        "add note", "create note", "new note", "make note",
        "add a note", "create a note", "make a note",
        "note about", "note that", "note:", "write note"
    ],
    "edit_note": [
        "edit note", "update note", "modify note", "change note"
    ],
    "delete_note": [
        "delete note", "remove note", "erase note"
    ],
    "show_notes": [
        "list my notes", "display notes", "my notes",
        "get notes", "view notes", "list notes"
    ],
    "add_note_tag": [
        "add tag", "tag note", "add note tag", "add tag to note",
        "tag to note", "attach tag"
    ],
    "remove_note_tag": [
        "remove tag", "delete tag", "remove note tag", "clear tag"
    ],
    "search_notes_text": [
        "search notes for", "find notes containing", "find notes with",
        "search note", "find note", "look up notes about"
    ],
    "search_notes_by_tag": [
        "notes with tag", "notes tagged", "notes by tag",
        "find notes with tag", "search notes by tag", "show notes with tag",
        "show notes tagged", "display notes with tag", "display notes tagged"
    ],
    "help": [
        "help", "commands", "what can you do", "how to use"
    ],
    "exit": [
        "exit", "quit", "close", "bye", "goodbye", "stop"
    ],
}

# Extended greeting keywords (not included in KEYWORD_MAP to avoid conflicts)
GREETING_KEYWORDS = [
    'hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon',
    'good evening', 'howdy', "what's up", "how's it going", 'how are you',
    'sup', 'yo', 'hiya', 'g\'day', 'aloha', 'salutations', 'good day'
]
"""Extended greeting keywords for hello intent (higher confidence than KEYWORD_MAP)."""
