import pytest
from pathlib import Path

from src.infrastructure.persistence.data_path_resolver import RESERVED_BASENAME
from src.infrastructure.storage.pickle_storage import PickleStorage
from src.infrastructure.storage.storage_type import StorageType


class SampleObject:
    """A simple custom object for testing pickling."""
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __eq__(self, other):
        return isinstance(other, SampleObject) and self.name == other.name and self.value == other.value


@pytest.fixture
def storage(tmp_path: Path) -> PickleStorage:
    """Provides a PickleStorage instance initialized in a temporary directory."""
    return PickleStorage(data_dir=tmp_path)


def test_initialization(tmp_path: Path):
    """Tests the constructor with and without a custom data directory."""
    storage_with_path = PickleStorage(data_dir=tmp_path)
    assert storage_with_path.resolver.data_dir == tmp_path

    storage_default = PickleStorage()
    assert storage_default.resolver.data_dir is not None
    assert storage_default.resolver.data_dir.exists()


def test_properties(storage: PickleStorage):
    """Tests the file_extension and storage_type properties."""
    assert storage.file_extension == '.pkl'
    assert storage.storage_type == StorageType.PICKLE


def test_save_and_load_successful(storage: PickleStorage):
    """Tests a standard save/load with a dictionary."""
    test_data = {"user": "test", "items": [1, 2, 3], "active": False}
    filename = "test_data_01"

    saved_filename = storage.save(test_data, filename)
    assert saved_filename == f"{filename}.pkl"

    expected_file = storage.resolver.data_dir / saved_filename
    assert expected_file.exists()
    assert expected_file.stat().st_size > 0

    loaded_data = storage.load(filename)
    assert loaded_data == test_data


def test_save_and_load_custom_object(storage: PickleStorage):
    """Tests saving and loading a custom Python object."""
    test_obj = SampleObject(name="test_obj", value=[1, "a", None])
    filename = "custom_object"

    storage.save(test_obj, filename)
    loaded_obj = storage.load(filename)

    assert loaded_obj == test_obj


def test_load_non_existent_file(storage: PickleStorage):
    """Tests loading a file that does not exist, expecting None."""
    assert storage.load("non_existent_file") is None


def test_load_empty_file(storage: PickleStorage):
    """Tests that loading an empty file returns None."""
    filename = "empty_file.pkl"
    filepath = storage.resolver.data_dir / filename
    filepath.touch()

    assert filepath.exists()
    assert filepath.stat().st_size == 0
    assert storage.load(filename) is None


def test_save_ensures_pkl_suffix(storage: PickleStorage):
    """Tests that the .pkl suffix is added if not present."""
    data = {"a": 1}
    saved_filename = storage.save(data, "test_file")
    assert saved_filename == "test_file.pkl"

    saved_filename_with_suffix = storage.save(data, "test_file_suffixed.pkl")
    assert saved_filename_with_suffix == "test_file_suffixed.pkl"


def test_load_with_invalid_pickle(storage: PickleStorage):
    """Tests that loading a file with corrupted data raises an IOError."""
    filename = "invalid.pkl"
    filepath = storage.resolver.data_dir / filename
    filepath.write_text("this is not a pickle stream")

    with pytest.raises(IOError, match="Failed to load data"):
        storage.load(filename)


def test_overwrite_existing_file(storage: PickleStorage):
    """Tests that saving to an existing filename overwrites the content."""
    filename = "overwrite_me"
    initial_data = SampleObject("v1", 1)
    new_data = SampleObject("v2", 2)

    storage.save(initial_data, filename)
    assert storage.load(filename) == initial_data

    storage.save(new_data, filename)
    assert storage.load(filename) == new_data


@pytest.mark.parametrize("invalid_filename", [
    "../invalid.pkl",
    "path/traversal.pkl",
    "another\\bad\\name.pkl"
])
def test_save_with_invalid_filename(storage: PickleStorage, invalid_filename: str):
    """Tests that attempting to save with a malicious filename raises an error."""
    with pytest.raises(ValueError, match="Filename must not contain directories"):
        storage.save({"data": "test"}, invalid_filename)


def test_user_provided_filename_is_checked(storage: PickleStorage):
    """Tests that `raise_if_reserved` is called for user-provided filenames."""
    reserved_filename = RESERVED_BASENAME
    data = {"a": 1}

    # Should raise error on save if user_provided is True
    with pytest.raises(ValueError, match="Filename '{}' is reserved. Please use a different name.".format(reserved_filename)):
        storage.save(data, reserved_filename, user_provided=True)

    # Should raise error on load if user_provided is True
    with pytest.raises(ValueError, match="Filename '{}' is reserved. Please use a different name.".format(reserved_filename)):
        storage.load(reserved_filename, user_provided=True)

    # Should NOT raise error if user_provided is False (the default)
    storage.save(data, reserved_filename)
    assert storage.load(reserved_filename) == data
