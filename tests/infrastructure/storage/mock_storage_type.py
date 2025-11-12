import os
import tempfile
from enum import Enum, auto
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional
import pytest
import sys
from unittest.mock import MagicMock, create_autospec

# This conftest.py creates mock objects for the dependencies of the storage classes.
# This allows the tests to run in isolation without needing the actual source code
# for the dependencies.

# Add the project root to the Python path to allow imports.
# You may need to adjust this path based on your project structure.
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


# --- Mock Implementation of Dependencies ---


class MockStorageType(Enum):
    """Mock of the StorageType Enum."""

    JSON = auto()
    YAML = auto()
    PICKLE = auto()
    SQLITE = auto()


class MockStorage(ABC):
    """Mock of the abstract base class Storage."""

    def __init__(self, *args, **kwargs):
        pass

    @property
    @abstractmethod
    def file_extension(self) -> str:
        pass

    @property
    @abstractmethod
    def storage_type(self) -> Any:
        pass

    @abstractmethod
    def save(self, data: Any, filename: str, **kwargs) -> str:
        pass

    @abstractmethod
    def load(self, filename: str, **kwargs) -> Optional[Any]:
        pass


class MockJsonStorage(MockStorage):
    def file_extension(self) -> str:
        return ".json"

    def storage_type(self) -> Any:
        return MockStorageType.JSON

    def save(self, data: Any, filename: str, **kwargs) -> str:
        return ""

    def load(self, filename: str, **kwargs) -> Optional[Any]:
        return None


class MockPickleStorage(MockStorage):
    def file_extension(self) -> str:
        return ".pkl"

    def storage_type(self) -> Any:
        return MockStorageType.PICKLE

    def save(self, data: Any, filename: str, **kwargs) -> str:
        return ""

    def load(self, filename: str, **kwargs) -> Optional[Any]:
        return None


class MockDBBase:
    """Mock for the DBBase domain model, including a mock metadata object."""

    metadata = MagicMock()


class MockSQLiteStorage(MockStorage):
    def __init__(self, db_base, data_dir=None):
        super().__init__(db_base, data_dir)
        self.db_base = db_base
        self.data_dir = data_dir

    def file_extension(self) -> str:
        return ".db"

    def storage_type(self) -> Any:
        return MockStorageType.SQLITE

    def save(self, data: Any, filename: str, **kwargs) -> str:
        return ""

    def load(self, filename: str, **kwargs) -> Optional[Any]:
        return None


class MockDataPathResolver:
    """A simplified mock of the DataPathResolver class."""

    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or Path(tempfile.gettempdir())
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def get_full_path(self, filename: str) -> Path:
        return self.data_dir / filename

    def ensure_json_suffix(self, filename: str):
        return filename

    def ensure_pkl_suffix(self, filename: str):
        return filename

    def raise_if_reserved(self, filename: str, reserved_set: set):
        pass

    def validate_filename(self, filename: str, allowed_extensions: tuple):
        pass


# Mocks for domain objects and mappers
class MockAddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name] = record


class MockNotebook:
    def __init__(self):
        self.data = {}

    def values(self):
        return self.data.values()


class MockContact:
    def __init__(self, name):
        self.name = name


class MockDBContact:
    pass


class MockNote:
    pass


class MockContactMapper:
    to_dbmodel = MagicMock()
    from_dbmodel = MagicMock()


class MockNoteMapper:
    to_dbmodel = MagicMock()


@pytest.fixture(autouse=True)
def mock_dependencies(monkeypatch):
    """This fixture automatically replaces the real dependencies with our mocks."""

    # Dummy modules to hold the mocked classes
    class DummyModule:
        pass

    # --- Mock external libraries ---
    mock_sqlalchemy = MagicMock()
    mock_sqlalchemy.orm.sessionmaker.return_value = MagicMock(return_value=MagicMock())
    sys.modules["sqlalchemy"] = mock_sqlalchemy
    sys.modules["sqlalchemy.orm"] = mock_sqlalchemy.orm

    # --- Mock project modules ---
    # Storage
    storage_module = DummyModule()
    setattr(storage_module, "Storage", MockStorage)
    setattr(storage_module, "StorageType", MockStorageType)
    setattr(storage_module, "JsonStorage", MockJsonStorage)
    setattr(storage_module, "PickleStorage", MockPickleStorage)
    setattr(
        storage_module, "SQLiteStorage", MockSQLiteStorage
    )  # Mock for factory tests
    sys.modules["src.storage.storage"] = storage_module
    sys.modules["src.storage.storage_type"] = storage_module
    sys.modules["src.storage.json_storage"] = storage_module
    sys.modules["src.storage.pickle_storage"] = storage_module
    sys.modules["src.storage.sqlite_storage"] = storage_module

    # Persistence
    persistence_module = DummyModule()
    setattr(persistence_module, "DataPathResolver", MockDataPathResolver)
    sys.modules["src.persistence.data_path_resolver"] = persistence_module

    # Domain
    dbbase_module = DummyModule()
    setattr(dbbase_module, "DBBase", MockDBBase)
    address_book_module = DummyModule()
    setattr(address_book_module, "AddressBook", MockAddressBook)
    notebook_module = DummyModule()
    setattr(notebook_module, "Notebook", MockNotebook)
    dbcontact_module = DummyModule()
    setattr(dbcontact_module, "DBContact", MockDBContact)
    contact_mapper_module = DummyModule()
    setattr(contact_mapper_module, "ContactMapper", MockContactMapper)
    note_mapper_module = DummyModule()
    setattr(note_mapper_module, "NoteMapper", MockNoteMapper)

    sys.modules["src.domain.models.dbbase"] = dbbase_module
    sys.modules["src.domain.address_book"] = address_book_module
    sys.modules["src.domain.notebook"] = notebook_module
    sys.modules["src.domain.models.dbcontact"] = dbcontact_module
    sys.modules["src.domain.mappers.contact_mapper"] = contact_mapper_module
    sys.modules["src.domain.mappers.note_mapper"] = note_mapper_module

    # Logging
    logging_module = DummyModule()
    setattr(logging_module, "setup_logger", MagicMock())
    sys.modules["src.logging.logger"] = logging_module


# Create dummy modules in sys.modules so imports can be resolved.
def setup_dummy_module(name):
    if name not in sys.modules:
        sys.modules[name] = __import__(name, fromlist=[""])


setup_dummy_module("src")
setup_dummy_module("src.infrastructure.logging")
setup_dummy_module("src.infrastructure.storage")
setup_dummy_module("src.infrastructure.persistence")
setup_dummy_module("src.domain")
setup_dummy_module("src.domain.models")
setup_dummy_module("src.domain.mappers")
