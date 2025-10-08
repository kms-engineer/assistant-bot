import os
import re
from pathlib import Path


APPLICATION_DIR = ".assistant-bot"
DEFAULT_DATA_DIR = "data"
HOME_DATA_DIR = Path.home() / APPLICATION_DIR / DEFAULT_DATA_DIR
RESERVED_BASENAME = "addressbook"
DEFAULT_CONTACTS_FILE = RESERVED_BASENAME + ".pkl"
DEFAULT_ADDRESS_BOOK_DATABASE_NAME = RESERVED_BASENAME + ".db"
DEFAULT_JSON_FILE = RESERVED_BASENAME + ".json"
DEFAULT_NOTES_FILE = "notes.json"


class DataPathResolver:

    def __init__(self, data_dir: Path = HOME_DATA_DIR):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def get_full_path(self, filename: str) -> Path:
        return self.data_dir / filename

    @staticmethod
    def ensure_pkl_suffix(filename: str) -> str:
        return filename if filename.endswith(".pkl") else f"{filename}.pkl"

    @staticmethod
    def ensure_json_suffix(filename: str) -> str:
        return filename if filename.endswith(".json") else f"{filename}.json"

    @staticmethod
    def ensure_db_suffix(filename: str) -> str:
        return filename if filename.endswith(".db") else f"{filename}.db"

    @staticmethod
    def validate_filename(filename: str, allowed_extensions: tuple = ('.pkl', '.json', '.db')) -> None:
        checks = [
            (not isinstance(filename, str) or not filename, "Filename must be a non-empty string"),
            (os.path.basename(filename) != filename, "Filename must not contain directories"),
            (len(filename) > 100, "Filename too long (max 100 characters)"),
            (filename.startswith('.'), "Filename must not start with '.'"),
            ('..' in filename, "Filename must not contain '..'"),
            (not re.fullmatch(r'[A-Za-z0-9_.-]+', filename), "Invalid characters in filename"),
            ('.' in filename and not any(filename.endswith(ext) for ext in allowed_extensions),
             f"Only {', '.join(allowed_extensions)} files are allowed"),
        ]
        for cond, msg in checks:
            if cond:
                raise ValueError(msg)

    @staticmethod
    def raise_if_reserved(filename: str, reserved_name: str = RESERVED_BASENAME) -> None:
        base = filename if '.' not in filename else filename.rsplit('.', 1)[0]
        if base == reserved_name or filename == f"{reserved_name}.pkl":
            raise ValueError(f"Filename '{reserved_name}' is reserved. Please use a different name.")
