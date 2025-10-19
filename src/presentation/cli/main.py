from src.domain.utils.styles_utils import stylize_text, stylize_error_message
from src.infrastructure.storage.storage_factory import StorageFactory
from src.infrastructure.storage.storage_type import StorageType
from .command_handler import CommandHandler
from .command_parser import CommandParser
from .ui_messages import UIMessages
from ...application.services.contact_service import ContactService
from ...application.services.note_service import NoteService  # Import NoteService
from ...infrastructure.persistence.data_path_resolver import *
from ...infrastructure.persistence.data_path_resolver import HOME_DATA_DIR, DEFAULT_DATA_DIR
from ...infrastructure.persistence.migrator import migrate_files
from ...infrastructure.storage.json_storage import JsonStorage
from ...infrastructure.storage.pickle_storage import PickleStorage
from ...infrastructure.storage.sqlite_storage import SQLiteStorage


def save_and_exit(service: ContactService, note_service: NoteService = None) -> None:
    print(UIMessages.SAVING)
    try:
        filename = contact_service.save_address_book()
        print(UIMessages.saved_successfully("Address book", filename))
    except Exception as e:
        print(stylize_error_message(message=f"Failed to save address book: {e}"))

    # Save notes if note_service provided
    if note_service:
        try:
            note_filename = note_service.save_notes()
            print(UIMessages.saved_successfully("Notes", note_filename))
        except Exception as e:
            print(stylize_error_message(message=f"Failed to save notes: {e}"))
        print(UIMessages.GOODBYE)


def main() -> None:
    # storage = PickleStorage()
    storage = JsonStorage()
    note_service = NoteService(storage)  # Initialize NoteService
    migrate_files(DEFAULT_DATA_DIR, HOME_DATA_DIR)
    storage_type = StorageType.SQLITE
    storage = StorageFactory.create_storage(storage_type)
    contact_service = ContactService(storage)
    # if storage_type == StorageType.SQLITE:
    #     note_service = NoteService(storage)
    # else:
    #     json_storage = JsonStorage()
    #     note_service = NoteService(json_storage)

    print(UIMessages.LOADING)
    try:
        count = 0
        if isinstance(storage, SQLiteStorage):
            count = contact_service.load_address_book(DEFAULT_ADDRESS_BOOK_DATABASE_NAME, user_provided=True)
        elif isinstance(storage, JsonStorage):
            count = contact_service.load_address_book(DEFAULT_JSON_FILE, user_provided=True)
        elif isinstance(storage, PickleStorage):
            count = contact_service.load_address_book(DEFAULT_CONTACTS_FILE, user_provided=True)
        print(UIMessages.loaded_successfully("Address book", count))
    except Exception as e:
        print(stylize_error_message(message=f"Failed to load address book: {e}. Starting with an empty book."))
    # Load notes
    try:
        note_count = note_service.load_notes()
        print(f"Loaded {note_count} notes successfully")
    except Exception as e:
        print(stylize_error_message(message=f"Failed to load notes: {e}. Starting with empty notes."))

    parser = CommandParser()
    handler = CommandHandler(contact_service, note_service)

    print(UIMessages.WELCOME + '\n\n' + UIMessages.COMMAND_LIST)

    while True:
        try:
            user_input = input(stylize_text("Enter a command: ")).strip()
            if not user_input:
                continue

            command, args = parser.parse(user_input)
            result = handler.handle(command, args)

            if result == "exit":
                save_and_exit(contact_service, note_service)
                break

            if result == "clear":
                continue

            print(result)

        except KeyboardInterrupt:
            print()
            save_and_exit(contact_service, note_service)
            break


if __name__ == "__main__":
    main()
