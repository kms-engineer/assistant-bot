from ...application.services.contact_service import ContactService
from ...infrastructure.storage.pickle_storage import PickleStorage
from ...infrastructure.storage.json_storage import JsonStorage
from .command_parser import CommandParser
from .command_handler import CommandHandler
from .ui_messages import UIMessages


def save_and_exit(service: ContactService) -> None:
    print(UIMessages.SAVING)
    try:
        filename = service.save_address_book()
        print(UIMessages.saved_successfully(filename))
    except Exception as e:
        print(f"Failed to save address book: {e}")
    print(UIMessages.GOODBYE)


def main() -> None:
    # storage = PickleStorage()
    storage = JsonStorage()
    contact_service = ContactService(storage)

    print(UIMessages.LOADING)
    try:
        count = contact_service.load_address_book()
        print(UIMessages.loaded_successfully(count))
    except Exception as e:
        print(f"Failed to load address book: {e}. Starting with an empty book.")

    parser = CommandParser()
    handler = CommandHandler(contact_service)

    print(UIMessages.WELCOME)

    while True:
        try:
            user_input = input("Enter a command: ").strip()
            if not user_input:
                continue

            command, args = parser.parse(user_input)
            result = handler.handle(command, args)

            if result == "exit":
                save_and_exit(contact_service)
                break

            print(result)

        except KeyboardInterrupt:
            print()
            save_and_exit(contact_service)
            break


if __name__ == "__main__":
    main()
