import argparse
from src.domain.utils.styles_utils import stylize_text, stylize_error_message
from src.infrastructure.storage.storage_factory import StorageFactory
from src.infrastructure.storage.storage_type import StorageType
from ...application.services.contact_service import ContactService
from ...application.services.note_service import NoteService
from ...infrastructure.storage.pickle_storage import PickleStorage
from ...infrastructure.storage.json_storage import JsonStorage
from ...infrastructure.persistence.migrator import migrate_files
from ...infrastructure.persistence.data_path_resolver import (
    HOME_DATA_DIR,
    DEFAULT_DATA_DIR,
    DEFAULT_ADDRESS_BOOK_DATABASE_NAME,
    DEFAULT_JSON_FILE,
    DEFAULT_CONTACTS_FILE
)
from ...infrastructure.storage.sqlite_storage import SQLiteStorage
from .command_parser import CommandParser
from .command_handler import CommandHandler
from .ui_messages import UIMessages
from .mode_decider import CLIMode
from .regex_gate import RegexCommandGate
from .input_processor import process_classic_input, process_nlp_input


def save_and_exit(contact_service: ContactService, note_service: NoteService = None, storage_type: StorageType = None) -> None:
    print(UIMessages.SAVING)

    # Save contacts
    try:
        filename = contact_service.save_address_book()
        if storage_type == StorageType.SQLITE:
            print(UIMessages.saved_successfully("Data", filename))
        else:
            print(UIMessages.saved_successfully("Address book", filename))
    except Exception as e:
        print(stylize_error_message(message=f"Failed to save address book: {e}"))

    # Save notes if note_service provided
    if note_service:
        try:
            note_filename = note_service.save_notes()
            # For SQLite, both are in the same file, so don't print duplicate message
            if storage_type != StorageType.SQLITE:
                print(UIMessages.saved_successfully("Notes", note_filename))
        except Exception as e:
            print(stylize_error_message(message=f"Failed to save notes: {e}"))

    print(UIMessages.GOODBYE)


def parse_cli_mode() -> CLIMode:
    arg_parser = argparse.ArgumentParser(description="Assistant Bot CLI")
    arg_parser.add_argument(
        "--mode",
        type=str,
        choices=["classic", "nlp"],
        default="classic",
        help="CLI mode: classic or nlp (default: classic)"
    )
    cli_args = arg_parser.parse_args()
    return CLIMode.from_string(cli_args.mode)


def main() -> None:
    mode = parse_cli_mode()

    migrate_files(DEFAULT_DATA_DIR, HOME_DATA_DIR)
    storage_type = StorageType.SQLITE
    storage = StorageFactory.create_storage(storage_type)
    contact_service = ContactService(storage)
    note_service = NoteService(storage)

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
    regex_gate = RegexCommandGate()

    # Initialize NLP manager for NLP mode
    nlp_manager = None
    is_nlp_mode = mode == CLIMode.NLP
    if is_nlp_mode:
        from .nlp_manager import NLPManager
        nlp_manager = NLPManager()
        nlp_manager.initialize_nlp_processor(use_pretrained=True)

    # Create handler with nlp_mode flag
    handler = CommandHandler(contact_service, note_service, nlp_mode=is_nlp_mode)

    # Show mode-appropriate help
    print(UIMessages.WELCOME + '\n\n' + UIMessages.get_command_list(is_nlp_mode))

    while True:
        try:
            user_input = input(stylize_text("Enter a command: ")).strip()
            if not user_input:
                continue

            if mode == CLIMode.CLASSIC:
                result = process_classic_input(user_input, parser, handler)
            elif mode == CLIMode.NLP:
                result = process_nlp_input(user_input, regex_gate, handler, nlp_manager)
                if not result:
                    print("Could not understand the command. Please try rephrasing or type 'help' for available commands.")
                    continue
            else:
                continue

            if result == "exit":
                save_and_exit(contact_service, note_service, storage_type)
                break

            if result == "clear":
                continue

            print(result)

        except KeyboardInterrupt:
            print()
            save_and_exit(contact_service, note_service, storage_type)
            break


if __name__ == "__main__":
    main()
