
class UIMessages:
    WELCOME = """Welcome to the assistant bot!

Available commands:
  hello                            - Show greeting
  add <name> <phone>               - Add new contact
  change <name> <old> <new>        - Update contact's phone
  phone <name>                     - Show contact's phone number(s)
  all                              - Show all contacts
  add-birthday <name> <DD.MM.YYYY> - Add birthday to contact
  show-birthday <name>             - Show contact's birthday
  birthdays                        - Show upcoming birthdays
  add-email <name> <email>         - Add email to contact
  add-address <name> <address>     - Add address to contact
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
    def invalid_command(available_commands: list) -> str:
        available = ', '.join(sorted(available_commands))
        return f"Invalid command. Available commands: {available}"
