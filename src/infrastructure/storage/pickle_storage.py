import os
import pickle
import tempfile
from pathlib import Path
from typing import Optional, Any
from .storage_interface import StorageInterface
from ..persistence.data_path_resolver import DataPathResolver, RESERVED_BASENAME


class PickleStorage(StorageInterface):

    def __init__(self, data_dir: Path = None):
        self.resolver = DataPathResolver(data_dir) if data_dir else DataPathResolver()

    @property
    def file_extension(self) -> str:
        return '.pkl'

    def save(self, data: Any, filename: str, **kwargs) -> str:
        user_provided = kwargs.get('user_provided', False)
        if user_provided:
            self.resolver.raise_if_reserved(filename, RESERVED_BASENAME)

        filename = self.resolver.ensure_pkl_suffix(filename)
        self.resolver.validate_filename(filename, allowed_extensions=('.pkl',))
        filepath = self.resolver.get_full_path(filename)

        tmp_file = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb",
                delete=False,
                dir=str(self.resolver.data_dir),
                prefix=Path(filename).stem + "_",
                suffix=".tmp"
            ) as tmp:
                tmp_file = Path(tmp.name)
                try:
                    os.chmod(tmp.name, 0o600)
                except OSError:
                    pass
                pickle.dump(data, tmp, protocol=pickle.HIGHEST_PROTOCOL)
                tmp.flush()
                os.fsync(tmp.fileno())

            os.replace(tmp_file, filepath)

            try:
                os.chmod(filepath, 0o600)
            except OSError:
                pass

            return filename

        except (OSError, pickle.PicklingError) as e:
            if tmp_file and tmp_file.exists():
                try:
                    tmp_file.unlink()
                except OSError:
                    pass
            raise IOError(f"Failed to save data: {e}") from e

    def load(self, filename: str, **kwargs) -> Optional[Any]:
        user_provided = kwargs.get('user_provided', False)
        if user_provided:
            self.resolver.raise_if_reserved(filename, RESERVED_BASENAME)

        filename = self.resolver.ensure_pkl_suffix(filename)
        self.resolver.validate_filename(filename, allowed_extensions=('.pkl',))
        filepath = self.resolver.get_full_path(filename)

        if not filepath.exists():
            return None

        try:
            if filepath.stat().st_size == 0:
                return None
        except OSError:
            return None

        try:
            with open(filepath, "rb") as f:
                return pickle.load(f)
        except (OSError, pickle.UnpicklingError, EOFError, AttributeError) as e:
            raise IOError(f"Failed to load data: {e}") from e
