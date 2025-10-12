from typing import Optional


class UIMessages:
    WELCOME = "Welcome to the assistant bot!"
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
  edit-email <name> <new email>    - Edit email adress in an existing contact
  remove-email <name>              - Remove email in an existing contact if set
  add-address <name> <address>     - Add address to contact
  edit-address <name> <address>    - Edit address in an existing contact
  remove-address <name>            - Remove addres in an existing contact if set
  save <filename>                  - Save address book to file
  load <filename>                  - Load address book from file
  close, exit                      - Exit the bot
"""

    GOODBYE = "Good bye!"
    SAVING = "Saving address book..."
    LOADING = "Loading address book..."

    @staticmethod
    def saved_successfully(filename: str) -> str:
        return f"Address book saved to file: {filename}"

    @staticmethod
    def loaded_successfully(count: int) -> str:
        return f"Address book loaded. {count} contact(s) found.\n"

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
