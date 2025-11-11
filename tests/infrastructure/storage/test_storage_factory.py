import pytest
from pathlib import Path

# The class to be tested
from src.infrastructure.storage.storage_factory import StorageFactory

# Mocked dependencies, which will be replaced by conftest.py
from src.infrastructure.storage.storage_type import StorageType
from src.infrastructure.storage.json_storage import JsonStorage
from src.infrastructure.storage.pickle_storage import PickleStorage
from src.infrastructure.storage.sqlite_storage import SQLiteStorage
from tests.infrastructure.storage.mock_storage_type import MockStorageType


def test_create_storage_json():
    """Tests that creating a JSON storage returns the correct type."""
    storage = StorageFactory.create_storage(StorageType.JSON)
    assert isinstance(storage, JsonStorage)


def test_create_storage_pickle():
    """Tests that creating a PICKLE storage returns the correct type."""
    storage = StorageFactory.create_storage(StorageType.PICKLE)
    assert isinstance(storage, PickleStorage)


def test_create_storage_sqlite():
    """Tests that creating a SQLITE storage returns the correct type."""
    storage = StorageFactory.create_storage(StorageType.SQLITE)
    assert isinstance(storage, SQLiteStorage)


def test_create_storage_with_none_type():
    """Tests that a ValueError is raised if the storage type is None."""
    with pytest.raises(ValueError, match="Storage type cannot be None."):
        StorageFactory.create_storage(None)


def test_create_storage_with_unsupported_type():
    """Tests that a ValueError is raised for an unsupported storage type."""
    with pytest.raises(ValueError, match="Unsupported storage type:"):
        StorageFactory.create_storage(MockStorageType.YAML)


@pytest.mark.parametrize(
    "filepath, expected_type",
    [
        ("data.json", JsonStorage),
        ("data.pkl", PickleStorage),
        ("data.pickle", PickleStorage),
        ("database.db", SQLiteStorage),
        ("database.sqlite", SQLiteStorage),
        ("database.sqlite3", SQLiteStorage),
    ],
)
def test_get_storage_by_extension(filepath, expected_type):
    """Tests getting the correct storage type based on file extension."""
    storage = StorageFactory.get_storage(filepath)
    assert isinstance(storage, expected_type)


def test_get_storage_with_unsupported_extension():
    """Tests that a ValueError is raised for an unsupported file extension."""
    filepath = "document.txt"
    with pytest.raises(
        ValueError,
        match="Only .pkl, .pickle, .json, .db, .sqlite, .sqlite3 files are allowed",
    ):
        StorageFactory.get_storage(filepath)


def test_get_storage_with_empty_filepath():
    """Tests that a ValueError is raised for an empty filepath."""
    empty_path = ""
    with pytest.raises(ValueError, match="Filename must be a non-empty string"):
        StorageFactory.get_storage(empty_path)
