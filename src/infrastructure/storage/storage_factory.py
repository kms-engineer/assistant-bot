from pathlib import Path

from src.infrastructure.storage.storage import Storage
from src.infrastructure.storage.json_storage import JsonStorage
from src.infrastructure.storage.pickle_storage import PickleStorage
from src.infrastructure.storage.sqlite_storage import SQLiteStorage
from src.infrastructure.storage.storage_type import StorageType
from src.infrastructure.persistence.data_path_resolver import DataPathResolver
from src.domain.models.dbbase import DBBase


class StorageFactory:

    @staticmethod
    def create_storage(storage_type: StorageType) -> Storage:
        if not storage_type:
            raise ValueError("Storage type cannot be None.")
        match storage_type:
            case StorageType.JSON:
                return JsonStorage()
            case StorageType.PICKLE:
                return PickleStorage()
            case StorageType.SQLITE:
                return SQLiteStorage(DBBase)
            case _:
                raise ValueError(f"Unsupported storage type: {storage_type}")

    @staticmethod
    def get_storage(filepath: str) -> Storage:
        DataPathResolver.validate_filename(filepath)
        storage_path = Path(filepath.lower())
        if storage_path.suffix.endswith(".json"):
            return JsonStorage(storage_path)
        elif storage_path.suffix.endswith(".pkl") or storage_path.suffix.endswith(
            ".pickle"
        ):
            return PickleStorage(storage_path)
        elif (
            storage_path.suffix.endswith(".db")
            or storage_path.suffix.endswith(".sqlite")
            or storage_path.suffix.endswith(".sqlite3")
        ):
            return SQLiteStorage(DBBase, storage_path)
        else:
            raise ValueError(
                f"Unsupported filetype: {storage_path}.\nSupported extensions: .json, .pkl, .pickle, .db, .sqlite, .sqlite3"
            )
