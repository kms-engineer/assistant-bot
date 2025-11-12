import json
import os
import tempfile
from pathlib import Path
from typing import Any, Optional

from .storage import Storage
from .storage_type import StorageType
from ..persistence.data_path_resolver import DataPathResolver


class JsonStorage(Storage):

    def __init__(self, data_dir: Path = None):
        self.resolver = DataPathResolver(data_dir) if data_dir else DataPathResolver()

    @property
    def file_extension(self) -> str:
        return ".json"

    @property
    def storage_type(self) -> StorageType:
        return StorageType.JSON

    def save(self, data: Any, filename: str, **kwargs) -> str:
        filename = self.resolver.ensure_json_suffix(filename)
        self.resolver.validate_filename(filename, allowed_extensions=(".json",))
        filepath = self.resolver.get_full_path(filename)

        tmp_file = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                delete=False,
                dir=str(self.resolver.data_dir),
                prefix=Path(filename).stem + "_",
                suffix=".tmp",
                encoding="utf-8",
            ) as tmp:
                tmp_file = Path(tmp.name)
                json.dump(data, tmp, ensure_ascii=False, indent=2)
                tmp.flush()
                os.fsync(tmp.fileno())

            os.replace(tmp_file, filepath)

            try:
                os.chmod(filepath, 0o600)
            except OSError:
                pass

            return filename

        except (OSError, TypeError, ValueError) as e:
            if tmp_file and tmp_file.exists():
                try:
                    tmp_file.unlink()
                except OSError:
                    pass
            raise IOError(f"Failed to save data to {filename}: {e}") from e

    def load(self, filename: str, **kwargs) -> Optional[Any]:
        default = kwargs.get("default", None)
        filename = self.resolver.ensure_json_suffix(filename)
        self.resolver.validate_filename(filename, allowed_extensions=(".json",))
        filepath = self.resolver.get_full_path(filename)

        if not filepath.exists():
            return default

        try:
            if filepath.stat().st_size == 0:
                return default
        except OSError:
            return default

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError, ValueError) as e:
            raise IOError(f"Failed to load data from {filename}: {e}") from e
