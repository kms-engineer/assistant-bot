from ...application.services.contact_service import ContactService
from ...application.services.note_service import NoteService  # Import NoteService
from ...infrastructure.storage.pickle_storage import PickleStorage
from ...infrastructure.storage.json_storage import JsonStorage
from ...infrastructure.persistence.migrator import migrate_files
from ...infrastructure.persistence.data_path_resolver import HOME_DATA_DIR, DEFAULT_DATA_DIR
from .command_parser import CommandParser
from .command_handler import CommandHandler
from .ui_messages import UIMessages


def save_and_exit(service: ContactService, note_service: NoteService = None) -> None:
    print(UIMessages.SAVING)
    try:
        filename = service.save_address_book()
        print(UIMessages.saved_successfully(filename))
    except Exception as e:
        print(f"Failed to save address book: {e}")

    # Save notes if note_service provided
    if note_service:
        try:
            note_filename = note_service.save_notes()
            print(f"Notes saved successfully to {note_filename}")
        except Exception as e:
            print(f"Failed to save notes: {e}")

    print(UIMessages.GOODBYE)


def main() -> None:
    # storage = PickleStorage()
    storage = JsonStorage()
    contact_service = ContactService(storage)
    note_service = NoteService(storage)  # Initialize NoteService

    migrate_files(DEFAULT_DATA_DIR, HOME_DATA_DIR)

    print(UIMessages.LOADING)
    try:
        count = contact_service.load_address_book()
        print(UIMessages.loaded_successfully(count))
    except Exception as e:
        print(f"Failed to load address book: {e}. Starting with an empty book.")

    # Load notes
    try:
        note_count = note_service.load_notes()
        print(f"Loaded {note_count} notes successfully")
    except Exception as e:
        print(f"Failed to load notes: {e}. Starting with empty notes.")

    parser = CommandParser()
    handler = CommandHandler(contact_service, note_service)

    print(UIMessages.WELCOME + '\n\n' + UIMessages.COMMAND_LIST)

    while True:
        try:
            user_input = input("Enter a command: ").strip()
            if not user_input:
                continue

            command, args = parser.parse(user_input)
            result = handler.handle(command, args)

            if result == "exit":
                save_and_exit(contact_service, note_service)
                break

            print(result)

        except KeyboardInterrupt:
            print()
            save_and_exit(contact_service, note_service)
            break


if __name__ == "__main__":
    main()
