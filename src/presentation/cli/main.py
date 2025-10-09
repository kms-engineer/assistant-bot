import argparse
from ...application.services.contact_service import ContactService
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


def process_nlp_input(user_input: str, regex_gate: RegexCommandGate, handler: CommandHandler) -> str:
    parsed = regex_gate.match(user_input)
    if not parsed:
        return ""
    command, args = parsed
    return handler.handle(command, args)


def main() -> None:
    mode = parse_cli_mode()

    storage = JsonStorage()
    contact_service = ContactService(storage)

    migrate_files(DEFAULT_DATA_DIR, HOME_DATA_DIR)

    print(UIMessages.LOADING)
    try:
        count = contact_service.load_address_book()
        print(UIMessages.loaded_successfully(count))
    except Exception as e:
        print(f"Failed to load address book: {e}. Starting with an empty book.")

    parser = CommandParser()
    handler = CommandHandler(contact_service)
    regex_gate = RegexCommandGate()

    print(UIMessages.WELCOME)

    while True:
        try:
            user_input = input("Enter a command: ").strip()
            if not user_input:
                continue

            if mode == CLIMode.CLASSIC:
                result = process_classic_input(user_input, parser, handler)
            elif mode == CLIMode.NLP:
                result = process_nlp_input(user_input, regex_gate, handler)
                if not result:
                    print("NLP Processing should be here.")
                    continue
            else:
                continue

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
