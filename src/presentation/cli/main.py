import argparse
from difflib import get_close_matches
from src.application.services.note_service import NoteService
from src.infrastructure.storage.storage_factory import StorageFactory
from src.infrastructure.storage.storage_type import StorageType
from ...domain.models.dbbase import DBBase
from ...infrastructure.persistence.data_path_resolver import *
from ...application.services.contact_service import ContactService
from ...application.services.note_service import NoteService
from ...infrastructure.storage.pickle_storage import PickleStorage
from ...infrastructure.storage.json_storage import JsonStorage
from ...infrastructure.persistence.migrator import migrate_files
from ...infrastructure.persistence.data_path_resolver import HOME_DATA_DIR, DEFAULT_DATA_DIR
from ...infrastructure.storage.sqlite_storage import SQLiteStorage
from .command_parser import CommandParser
from .command_handler import CommandHandler
from .ui_messages import UIMessages
from .mode_decider import CLIMode
from .regex_gate import RegexCommandGate


def save_and_exit(contact_service: ContactService, note_service: NoteService = None) -> None:
    print(UIMessages.SAVING)
    try:
        filename = contact_service.save_address_book()
        print(UIMessages.saved_successfully("Address book", filename))
    except Exception as e:
        print(f"Failed to save address book: {e}")

    # Save notes if note_service provided
    if note_service:
        try:
            note_filename = note_service.save_notes()
            print(UIMessages.saved_successfully("Notes", note_filename))
        except Exception as e:
            print(f"Failed to save notes: {e}")
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


def process_classic_input(user_input: str, parser: CommandParser, handler: CommandHandler) -> str:
    command, args = parser.parse(user_input)
    return handler.handle(command, args)


def process_nlp_input(user_input: str, regex_gate: RegexCommandGate, handler: CommandHandler, nlp_manager=None) -> str:
    # First try regex matching
    parsed = regex_gate.match(user_input)
    if parsed:
        command, args = parsed
        return handler.handle(command, args)

    # If regex fails, try NLP processing
    if nlp_manager and nlp_manager.is_ready():
        try:
            nlp_result = nlp_manager.process_input(user_input, verbose=False)

            if nlp_result is None:
                # NLP processor not available - suggest similar commands
                return _get_nlp_failure_message(user_input, handler)

            # Check confidence - if very low, suggest commands
            confidence = nlp_result.get('confidence', 0.0)
            LOW_CONFIDENCE_THRESHOLD = 0.55  # If confidence < 0.55, suggest alternatives

            if confidence < LOW_CONFIDENCE_THRESHOLD:
                # Low confidence result - might be wrong, suggest alternatives
                suggestion_msg = _get_nlp_failure_message(user_input, handler)
                return f"Low confidence understanding (confidence: {confidence:.2f}).\n{suggestion_msg}"

            # Check if validation passed
            if nlp_result.get('validation', {}).get('valid', False):
                command, args = nlp_manager.get_command_args(nlp_result)
                return handler.handle(command, args)
            else:
                # Show what was understood and what's missing
                missing = nlp_result.get('validation', {}).get('missing', [])
                errors = nlp_result.get('validation', {}).get('errors', [])

                response = f"I understood your intent as '{nlp_result['intent']}'"
                if nlp_result['entities']:
                    response += f" with: {nlp_result['entities']}"

                if missing:
                    response += f"\n\nMissing required information: {', '.join(missing)}"
                if errors:
                    response += f"\n\nValidation errors: {'; '.join(errors)}"

                return response
        except Exception as e:
            # NLP processing failed - suggest similar commands
            return _get_nlp_failure_message(user_input, handler, error=str(e))

    # NLP manager not available
    return _get_nlp_failure_message(user_input, handler)


def _get_nlp_failure_message(user_input: str, handler: CommandHandler, error: str = None) -> str:
    # Get example phrases for NLP
    examples = handler.get_nlp_command_examples()

    # Try to find similar command examples
    suggestions = get_close_matches(user_input.lower(), examples, n=1, cutoff=0.6)

    base_message = "Could not understand the command."
    if error:
        base_message = f"NLP processing error: {error}"

    if suggestions:
        return f"{base_message}\n\nDid you mean: \"{suggestions[0]}\"?\n\nType 'help' for all available commands."
    else:
        return f"{base_message}\n\nPlease try rephrasing or type 'help' for available commands."


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
        print(f"Failed to load address book: {e}. Starting with an empty book.")

    # Load notes
    try:
        note_count = note_service.load_notes()
        print(f"Loaded {note_count} notes successfully")
    except Exception as e:
        print(f"Failed to load notes: {e}. Starting with empty notes.")

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
            user_input = input("Enter a command: ").strip()
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
                save_and_exit(contact_service, note_service)
                break

            print(result)

        except KeyboardInterrupt:
            print()
            save_and_exit(contact_service, note_service)
            break


if __name__ == "__main__":
    main()
