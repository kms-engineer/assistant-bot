import argparse
from ...application.services.contact_service import ContactService
from ...application.services.note_service import NoteService
from ...infrastructure.storage.pickle_storage import PickleStorage
from ...infrastructure.storage.json_storage import JsonStorage
from ...infrastructure.persistence.migrator import migrate_files
from ...infrastructure.persistence.data_path_resolver import HOME_DATA_DIR, DEFAULT_DATA_DIR
from .command_parser import CommandParser
from .command_handler import CommandHandler
from .ui_messages import UIMessages
from .mode_decider import CLIMode
from .regex_gate import RegexCommandGate


def save_and_exit(service: ContactService) -> None:
    print(UIMessages.SAVING)
    try:
        filename = service.save_address_book()
        print(UIMessages.saved_successfully(filename))
    except Exception as e:
        print(f"Failed to save address book: {e}")
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
                return "NLP processor not available. Please try rephrasing your command."

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
            return f"NLP processing error: {e}\nPlease try rephrasing your command."

    return ""


def main() -> None:
    mode = parse_cli_mode()

    storage = JsonStorage()
    contact_service = ContactService(storage)
    note_service = NoteService(storage)

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
        print(f"Loaded {note_count} notes.")
    except Exception as e:
        print(f"Failed to load notes: {e}. Starting with empty notes.")

    parser = CommandParser()
    handler = CommandHandler(contact_service)
    regex_gate = RegexCommandGate()

    # Initialize NLP manager for NLP mode
    nlp_manager = None
    if mode == CLIMode.NLP:
        from .nlp_manager import NLPManager
        nlp_manager = NLPManager()
        nlp_manager.initialize_nlp_processor(use_pretrained=True)

    print(UIMessages.WELCOME + '\n\n' + UIMessages.COMMAND_LIST)

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
                save_and_exit(contact_service)
                # Save notes too
                try:
                    note_service.save_notes()
                    print("Notes saved successfully.")
                except Exception as e:
                    print(f"Failed to save notes: {e}")
                break

            print(result)

        except KeyboardInterrupt:
            print()
            save_and_exit(contact_service)
            # Save notes
            try:
                note_service.save_notes()
            except:
                pass
            break


if __name__ == "__main__":
    main()
