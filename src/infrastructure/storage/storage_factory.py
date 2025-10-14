from pathlib import Path

from .storage import Storage
from .json_storage import JsonStorage
from .pickle_storage import PickleStorage
from .sqlite_storage import SQLiteStorage
from .storage_type import StorageType
from ..persistence.data_path_resolver import DataPathResolver
from ...domain.models.dbbase import DBBase


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
        filepath = Path(filepath.lower())
        if filepath.suffix.endswith('.json'):
            return JsonStorage(filepath)
        elif filepath.suffix.endswith('.pkl') or filepath.suffix.endswith('.pickle'):
            return PickleStorage(filepath)
        elif filepath.suffix.endswith('.db') or filepath.suffix.endswith('.sqlite') or filepath.suffix.endswith('.sqlite3'):
            return SQLiteStorage(DBBase, filepath)
        else:
            raise ValueError(f"Unsupported filetype: {filepath}.\nSupported extensions: .json, .pkl, .pickle, .db, .sqlite, .sqlite3")
