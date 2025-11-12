import json
import pytest
from pathlib import Path
from typing import Any

from src.infrastructure.storage.json_storage import JsonStorage
from src.infrastructure.storage.storage_type import StorageType


@pytest.fixture
def storage(tmp_path: Path) -> JsonStorage:
    """Provides a JsonStorage instance initialized in a temporary directory."""
    return JsonStorage(data_dir=tmp_path)


def test_initialization(tmp_path: Path):
    """Tests the constructor with and without a custom data directory."""
    # Test with a specific data directory
    storage_with_path = JsonStorage(data_dir=tmp_path)
    assert storage_with_path.resolver.data_dir == tmp_path

    # Test with default directory (relies on the mock resolver's default)
    storage_default = JsonStorage()
    assert storage_default.resolver.data_dir is not None
    assert storage_default.resolver.data_dir.exists()


def test_properties(storage: JsonStorage):
    """Tests the file_extension and storage_type properties."""
    assert storage.file_extension == ".json"
    assert storage.storage_type == StorageType.JSON


def test_save_and_load_successful(storage: JsonStorage):
    """Tests a standard save operation followed by a load operation."""
    test_data = {"user": "test", "items": [1, 2, {"key": "value"}], "active": True}
    filename = "test_data_01"

    # Save the data
    saved_filename = storage.save(test_data, filename)
    assert saved_filename == f"{filename}.json"

    # Check that the file was created in the correct directory
    expected_file = storage.resolver.data_dir / saved_filename
    assert expected_file.exists()
    assert expected_file.stat().st_size > 0

    # Load the data back
    loaded_data = storage.load(filename)
    assert loaded_data == test_data


def test_load_non_existent_file(storage: JsonStorage):
    """Tests loading a file that does not exist, expecting the default value."""
    # Default is None
    assert storage.load("non_existent_file") is None

    # With a custom default value
    custom_default = {"default": True}
    assert storage.load("non_existent_file", default=custom_default) == custom_default


def test_load_empty_file(storage: JsonStorage):
    """Tests that loading an empty file returns the default value."""
    filename = "empty_file.json"
    filepath = storage.resolver.data_dir / filename
    filepath.touch()  # Create an empty file

    assert filepath.exists()
    assert filepath.stat().st_size == 0

    assert storage.load(filename) is None
    assert storage.load(filename, default=[]) == []


def test_save_ensures_json_suffix(storage: JsonStorage):
    """Tests that the .json suffix is added if not present."""
    data = {"a": 1}
    # Filename without suffix
    saved_filename = storage.save(data, "test_file")
    assert saved_filename == "test_file.json"

    # Filename with suffix
    saved_filename_with_suffix = storage.save(data, "test_file_suffixed.json")
    assert saved_filename_with_suffix == "test_file_suffixed.json"


def test_save_with_non_serializable_data(storage: JsonStorage):
    """Tests that saving non-JSON-serializable data raises an IOError."""
    non_serializable_data = {1, 2, 3}  # A set is not serializable
    with pytest.raises(IOError, match="Failed to save data to test_set.json"):
        storage.save(non_serializable_data, "test_set")


def test_load_with_invalid_json(storage: JsonStorage):
    """Tests that loading a file with corrupted JSON raises an IOError."""
    filename = "invalid.json"
    filepath = storage.resolver.data_dir / filename
    filepath.write_text("{'key': 'this is not valid json'}")

    with pytest.raises(IOError, match="Failed to load data from invalid.json"):
        storage.load(filename)


def test_save_and_load_with_unicode(storage: JsonStorage):
    """Tests that non-ASCII characters are handled correctly."""
    unicode_data = {"name": "Jörg", "city": "København", "currency": "€"}
    filename = "unicode_test"

    storage.save(unicode_data, filename)
    loaded_data = storage.load(filename)

    assert loaded_data == unicode_data


def test_overwrite_existing_file(storage: JsonStorage):
    """Tests that saving to an existing filename overwrites the content."""
    filename = "overwrite_me"
    initial_data = {"version": 1}
    new_data = {"version": 2, "status": "updated"}

    # First save
    storage.save(initial_data, filename)
    assert storage.load(filename) == initial_data

    # Second save
    storage.save(new_data, filename)
    assert storage.load(filename) == new_data


@pytest.mark.parametrize(
    "invalid_filename",
    ["../invalid.json", "data/storage.json", "another\\bad\\name.json"],
)
def test_save_with_invalid_filename(storage: JsonStorage, invalid_filename: str):
    """Tests that attempting to save with a malicious filename raises an error."""
    with pytest.raises(ValueError, match="Filename must not contain directories"):
        storage.save({"data": "test"}, invalid_filename)
