from typing import Optional

from src.domain.utils.styles_utils import (
    stylize_success,
    stylize_errors,
    stylize_warning,
)


class UIMessages:
    WELCOME = "Welcome to the assistant bot!"

    # Classic mode command list (technical format)
    COMMAND_LIST = """Available commands:

GENERAL:
  hello                            - Show greeting
  help                             - Show commands list
  clear                            - Clear the command-line interface
  close, exit                      - Exit the bot

CONTACTS:
  add <name> <phone>               - Add new contact
  all                              - Show all contacts
  change <name> <old> <new>        - Update contact's phone
  delete-contact <name>            - Delete contact
  find <search_text>               - Find exact matching names/emails/phones
  phone <name>                     - Show contact's phone number(s)
  remove-phone <name> <phone>      - Remove phone from contact
  search <search_text>             - Search matching (not strict) names/emails/phones

EMAIL:
  add-email <name> <email>         - Add email to contact
  edit-email <name> <new email>    - Edit email address in an existing contact
  remove-email <name>              - Remove email in an existing contact if set

ADDRESS:
  add-address <name> <address>     - Add address to contact
  edit-address <name> <address>    - Edit address in an existing contact
  remove-address <name>            - Remove address in an existing contact if set

BIRTHDAY:
  add-birthday <name> <DD.MM.YYYY> - Add birthday to contact
  birthdays <amount>               - Show upcoming birthdays for <amount> days ahead or 7 days by default (max=365)
  remove-birthday <name>           - Remove birthday from contact
  show-birthday <name>             - Show contact's birthday

NOTES:
  add-note <title> <text>          - Add new note with title and text
  add-tag <id> <tag>               - Add a tag to a note
  delete-note <id>                 - Delete note by ID
  delete-note-by-tag <tag>         - Delete all notes with specific tag
  delete-note-by-title <title>     - Delete note(s) by title
  edit-note <id> <new text>        - Edit note text by ID
  list-tags                        - List all tags with usage count
  remove-tag <id> <tag>            - Remove a tag from a note
  rename-note <id> <new title>     - Rename note by ID
  search-notes <query>             - Search notes by text content
  search-notes-by-tag <tag>        - Search notes by tag
  search-notes-by-title <query>    - Search notes by title
  show-note <id>                   - Show specific note by ID
  show-notes                       - Show all notes
  show-notes --sort-by-tag         - Show all notes grouped by tags

FILE OPERATIONS:
  load <filename>                  - Load address book from file
  save <filename>                  - Save address book to file
"""

    # NLP mode command list (natural language format)
    NLP_COMMAND_LIST = """
══════════════════════════════════════════════════════════════════════════
                       NATURAL LANGUAGE COMMANDS
══════════════════════════════════════════════════════════════════════════

CONTACTS:
  Show all contacts                                    - List all contacts
  Add John 321-555-1234                                - Add new contact
  Search contact John                                  - Search contacts
  Search john@example.com                              - Find by email
  Delete contact John                                  - Remove contact
  Show John phone                                      - Display phone

PHONE:
  Add John 321-555-1234                                  - Add phone number
  Change John phone from 321-555-1234 to 321-555-9999    - Update phone
  Remove phone 555-1234 from John                        - Delete phone

EMAIL:
  Add email john@example.com to John                   - Add email
  Change John's email to new@mail.com                  - Update email
  Remove email from John                               - Delete email

ADDRESS:
  Add address 123 Main St Apt 5B, Chicago, IL 60601   - Add address
  Change John's address to 456 Oak Ave, Austin, TX    - Update address
  Remove address from John                            - Delete address

BIRTHDAY:
  Add birthday 15.03.1990 to John                      - Set birthday
  Show birthdays for next 30 days                      - Upcoming birthdays
  Remove birthday from John                            - Delete birthday

NOTES:
  Show all notes                                              - List all notes
  Show note a1b2c3d4-e5f6-7890-abcd-ef1234567890              - Display note by ID
  Add tag #work to note a1b2c3d4-e5f6-7890-abcd-ef123...      - Tag a note
  Remove tag #work from note a1b2c3d4-e5f6-7890-abcd-...      - Remove tag
  Show all tags                                               - List all tags
  Search notes meeting                                        - Find by text
  Search notes by tag #work                                   - Find by tag

GENERAL:
  Hello                                                - Greeting
  Help                                                 - Show this help
  Clear screen                                         - Clear console
  Exit                                                 - Close the bot
══════════════════════════════════════════════════════════════════════════
"""

    GOODBYE = "Good bye!"
    SAVING = "Saving address book..."
    LOADING = "Loading address book..."

    # Confirmation prompts (friendly but clear)
    CONFIRM_DELETE_CONTACT = "Delete contact '{name}'? This can't be undone"
    CONFIRM_REMOVE_EMAIL = "Remove email from '{name}'?"
    CONFIRM_REMOVE_ADDRESS = "Remove address from '{name}'?"
    CONFIRM_LOAD_FILE = "Loading will replace your current data. Want to continue?"

    # Cancellation messages
    ACTION_CANCELLED = "No worries, cancelled that for you."

    @staticmethod
    def get_command_list(nlp_mode: bool = False) -> str:
        return UIMessages.NLP_COMMAND_LIST if nlp_mode else UIMessages.COMMAND_LIST

    @staticmethod
    @stylize_success
    def saved_successfully(entity: str, filename: str) -> str:
        return f"{entity} saved to file: {filename}"

    @staticmethod
    @stylize_success
    def loaded_successfully(entity: str, count: int) -> str:
        return f"{entity} loaded. {count} contact(s) found.\n"

    @staticmethod
    @stylize_errors
    def error(message: str) -> str:
        return f"Error: {message}"

    @staticmethod
    @stylize_warning
    def invalid_command(
        available_commands: list, suggestion: Optional[str] = None
    ) -> str:
        available = ", ".join(sorted(available_commands))
        if suggestion:
            return (
                f"Invalid command. Did you mean '{suggestion}'? \n"
                f"Available commands: {available}"
            )
        return f"Invalid command. Available commands: {available}"
