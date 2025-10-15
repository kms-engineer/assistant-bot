from src.application.services.note_service import NoteService
from src.infrastructure.storage.storage_factory import StorageFactory
from src.infrastructure.storage.storage_type import StorageType
from ...domain.models.dbbase import DBBase
from ...infrastructure.persistence.data_path_resolver import *
from ...application.services.contact_service import ContactService
from ...infrastructure.storage.pickle_storage import PickleStorage
from ...infrastructure.storage.json_storage import JsonStorage
from ...infrastructure.persistence.migrator import migrate_files
from ...infrastructure.persistence.data_path_resolver import HOME_DATA_DIR, DEFAULT_DATA_DIR
from ...infrastructure.storage.sqlite_storage import SQLiteStorage
from .command_parser import CommandParser
from .command_handler import CommandHandler
from .ui_messages import UIMessages


def save_and_exit(contact_service: ContactService, note_service: NoteService) -> None:
    print(UIMessages.SAVING)
    try:
        filename = contact_service.save_address_book()
        print(UIMessages.saved_successfully("Address book", filename))
    except Exception as e:
        print(f"Failed to save address book: {e}")
    try:
        note_filename = note_service.save_notes()
        print(UIMessages.saved_successfully("Notes", note_filename))
    except Exception as e:
        print(f"Failed to save notes: {e}")
    print(UIMessages.GOODBYE)


def main() -> None:
    migrate_files(DEFAULT_DATA_DIR, HOME_DATA_DIR)
    storage_type = StorageType.SQLITE
    storage = StorageFactory.create_storage(storage_type)
    contact_service = ContactService(storage)
    # if storage_type == StorageType.SQLITE:
    #     note_service = NoteService(storage)
    # else:
    #     json_storage = JsonStorage()
    #     note_service = NoteService(json_storage)
    json_storage = JsonStorage()
    note_service = NoteService(json_storage)

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
        print(f"Failed to load address book: {e}. Starting with an empty book.")

    parser = CommandParser()
    handler = CommandHandler(contact_service)

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
