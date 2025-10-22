from typing import Optional

from src.domain.utils.styles_utils import stylize_success, stylize_errors, stylize_warning


class UIMessages:
    WELCOME = "Welcome to the assistant bot!"
    COMMAND_LIST = """Available commands:
  hello                            - Show greeting
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
  search <search_text>             - Search matching (not strict) names/emails/phones
  find <search_text>               - Find exact matching names/emails/phones
  add-note <text>                  - Add new note
  show-notes                       - Show all notes
  edit-note <id> <new text>        - Edit note by ID
  delete-note <id>                 - Delete note by ID
  
  save <filename>                  - Save address book to file
  load <filename>                  - Load address book from file
  
  clear                            - Clear the command-line interface
  help                             - Show commands list
  close, exit                      - Exit the bot
"""

    GOODBYE = "Good bye!"
    SAVING = "Saving address book..."
    LOADING = "Loading address book..."

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
    def invalid_command(available_commands: list, suggestion: Optional[str] = None) -> str:
        available = ', '.join(sorted(available_commands))
        if suggestion:
            return (f"Invalid command. Did you mean '{suggestion}'? \n"
                    f"Available commands: {available}")
        return f"Invalid command. Available commands: {available}"
