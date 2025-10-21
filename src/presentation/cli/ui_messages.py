from typing import Optional


class UIMessages:
    WELCOME = "Welcome to the assistant bot!"

    # Classic mode command list (technical format)
    COMMAND_LIST = """Available commands:
  hello                            - Show greeting
  help                             - Show commands list
  add <name> <phone>               - Add new contact
  change <name> <old> <new>        - Update contact's phone
  delete-contact <name>            - Delete contact
  phone <name>                     - Show contact's phone number(s)
  all                              - Show all contacts
  add-birthday <name> <DD.MM.YYYY> - Add birthday to contact
  show-birthday <name>             - Show contact's birthday
  birthdays <amount>               - Show upcoming birthdays for <amount> days ahead or 7 days by default (max=365)
  add-email <name> <email>         - Add email to contact
  edit-email <name> <new email>    - Edit email address in an existing contact
  remove-email <name>              - Remove email in an existing contact if set
  add-address <name> <address>     - Add address to contact
  edit-address <name> <address>    - Edit address in an existing contact
  remove-address <name>            - Remove address in an existing contact if set
  save <filename>                  - Save address book to file
  load <filename>                  - Load address book from file
  search <search_text>             - Search matching (not strict) names/emails/phones
  find <search_text>               - Find exact matching names/emails/phones
  add-note <text>                  - Add new note
  show-notes                       - Show all notes
  edit-note <id> <new text>        - Edit note by ID
  delete-note <id>                 - Delete note by ID
  add-tag <note_id> <tag>          - Add tag to note
  remove-tag <note_id> <tag>       - Remove tag from note
  search-notes <query>             - Search notes by text content
  search-by-tag <tag>              - Search notes by tag
  close, exit                      - Exit the bot
"""

    # NLP mode command list (natural language format)
    NLP_COMMAND_LIST = """You can talk to me naturally! Here are some things you can say:

📇 CONTACT MANAGEMENT:
  • "Add <name> to my contacts with phone <phone>" (name and phone required)
  • "Add <name> with phone <phone> and birthday <DD.MM.YYYY>"
  • "Add <name> with phone <phone> and email <email>"
  • "Add <name> with phone <phone> from <address>"
  • "Change phone for <name> from <old phone> to <new phone>"
  • "Delete contact <name>"
  • "Show phone for <name>"
  • "Show all contacts"

🎂 BIRTHDAYS:
  • "Add birthday <DD.MM.YYYY> for <name>"
  • "Show birthday for <name>"
  • "Show upcoming birthdays" (for next 7 days)
  • "Show birthdays for next <days> days" (max 365 days)

📧 EMAIL & ADDRESS:
  • "Add email <email> for <name>"
  • "Edit email for <name> to <new email>"
  • "Remove email from <name>"
  • "Add address <address> for <name>"
  • "Edit address for <name> to <new address>"
  • "Remove address from <name>"

🔍 SEARCH:
  • "Search for <text>" (partial match in names, emails, phones)
  • "Find exact <text>" (exact match only)

📝 NOTES:
  • "Add note: <text>"
  • "Show all notes"
  • "Edit note <id> with text: <new text>"
  • "Delete note <id>"
  • "Add tag <tag> to note <id>"
  • "Remove tag <tag> from note <id>"
  • "Search notes for <query>"
  • "Find notes with tag <tag>"

💾 FILE OPERATIONS:
  • "Save contacts to <filename>"
  • "Load contacts from <filename>"

❓ HELP & EXIT:
  • "Help" or "Show commands"
  • "Exit" or "Goodbye" or "Close"

💡 TIP: You can use natural language! For example:
   Instead of: "add John 1234567890"
   Just say: "Add John to my contacts with phone 1234567890"
"""

    GOODBYE = "Good bye!"
    SAVING = "Saving address book..."
    LOADING = "Loading address book..."

    @staticmethod
    def get_command_list(nlp_mode: bool = False) -> str:
        """Get command list based on mode."""
        return UIMessages.NLP_COMMAND_LIST if nlp_mode else UIMessages.COMMAND_LIST

    @staticmethod
    def saved_successfully(entity: str, filename: str) -> str:
        return f"{entity} saved to file: {filename}"

    @staticmethod
    def loaded_successfully(entity: str, count: int) -> str:
        return f"{entity} loaded. {count} contact(s) found.\n"

    @staticmethod
    def error(message: str) -> str:
        return f"Error: {message}"

    @staticmethod
    def invalid_command(available_commands: list, suggestion: Optional[str] = None) -> str:
        available = ', '.join(sorted(available_commands))
        if suggestion:
            return (f"Invalid command. Did you mean '{suggestion}'? \n"
                    f"Available commands: {available}")
        return f"Invalid command. Available commands: {available}"
