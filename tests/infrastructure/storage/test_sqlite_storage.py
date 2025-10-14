# import pytest
# from unittest.mock import MagicMock, patch, ANY
#
# # The class to be tested
# from src.infrastructure.storage.sqlite_storage import SQLiteStorage
# # Mocked dependencies, which will be replaced by conftest.py
# from src.infrastructure.storage.storage_type import StorageType
# from src.domain.models.dbbase import DBBase
# from src.domain.address_book import AddressBook
# from src.domain.notebook import Notebook
# from src.domain.mappers.contact_mapper import ContactMapper
# from src.domain.mappers.note_mapper import NoteMapper
# from src.domain.models.dbcontact import DBContact
# from tests.infrastructure.storage.mock_storage_type import MockDBBase
#
#
# class MockContact:
#     def __init__(self, name):
#         self.name = name
#
#
# class MockNote:
#     def __init__(self, title):
#         self.title = title
#
#
# @pytest.fixture
# def mock_db_base():
#     """Provides a mock DBBase class."""
#     # Reset metadata calls for each test
#     MockDBBase.metadata.create_all.reset_mock()
#     return DBBase
#
#
# @pytest.fixture
# def storage(mock_db_base):
#     """Provides a SQLiteStorage instance for testing."""
#     return SQLiteStorage(base=mock_db_base)
#
#
# @patch('src.infrastructure.storage.sqlite_storage.create_engine')
# @patch('src.infrastructure.storage.sqlite_storage.sessionmaker')
# # @patch('src.domain.models.dbbase.DBBase')
# def test_initialize(mock_sessionmaker, mock_create_engine, storage, mock_db_base, tmp_path):
#     """Tests the database initialization process."""
#     storage.resolver.data_dir = tmp_path
#     db_name = "test.db"
#
#     storage.initialize(db_name)
#
#     expected_db_path = tmp_path / db_name
#     mock_create_engine.assert_called_once_with(f"sqlite:///{expected_db_path}", echo=False, future=True)
#     mock_sessionmaker.assert_called_once_with(bind=mock_create_engine.return_value, expire_on_commit=False)
#     mock_db_base.metadata.create_all.assert_called_once_with(mock_create_engine.return_value)
#     assert storage._is_initialized
#
#
# def test_create_session_uninitialized(storage):
#     """Tests that creating a session before initialization raises an error."""
#     with pytest.raises(RuntimeError, match="SQLiteStorage is not initialized"):
#         storage._create_session()
#
#
# def test_properties(storage):
#     """Tests the basic properties of the storage class."""
#     assert storage.file_extension == ".db"
#     assert storage.storage_type == StorageType.SQLITE
#
#
# def test_save_entity(storage):
#     """Tests the generic entity saving method."""
#     mock_session = MagicMock()
#     storage._create_session = MagicMock(return_value=mock_session)
#
#     entity = {"id": 1, "data": "test"}
#     storage.save_entity(entity)
#
#     mock_session.__enter__.return_value.merge.assert_called_once_with(entity)
#     mock_session.__enter__.return_value.commit.assert_called_once()
#     mock_session.__enter__.return_value.expunge.assert_called_once()
#
#
# def test_get_all(storage):
#     """Tests the generic get_all method."""
#     mock_session = MagicMock()
#     storage._create_session = MagicMock(return_value=mock_session)
#
#     storage.get_all(DBContact)
#
#     mock_session.__enter__.return_value.query.assert_called_once_with(DBContact)
#     mock_session.__enter__.return_value.query.return_value.all.assert_called_once()
#     mock_session.__enter__.return_value.expunge_all.assert_called_once()
#
#
# @patch.object(SQLiteStorage, 'initialize')
# @patch.object(SQLiteStorage, 'save_entity')
# def test_save_addressbook(mock_save_entity, mock_initialize, storage):
#     """Tests saving an AddressBook object."""
#     mock_contact1 = MockContact("John")
#     mock_contact2 = MockContact("Jane")
#
#     address_book = AddressBook()
#     address_book.data = {"John": mock_contact1, "Jane": mock_contact2}
#
#     ContactMapper.to_dbmodel.side_effect = [DBContact(), DBContact()]
#
#     filename = "contacts.db"
#     storage.save(address_book, filename)
#
#     mock_initialize.assert_called_once_with(db_name=filename)
#     assert mock_save_entity.call_count == 2
#     ContactMapper.to_dbmodel.assert_any_call(mock_contact1)
#     ContactMapper.to_dbmodel.assert_any_call(mock_contact2)
#
#
# @patch.object(SQLiteStorage, 'initialize')
# @patch.object(SQLiteStorage, 'get_all')
# def test_load_addressbook(mock_get_all, mock_initialize, storage):
#     """Tests loading data into an AddressBook."""
#     mock_db_contact1 = DBContact()
#     mock_db_contact2 = DBContact()
#     mock_get_all.return_value = [mock_db_contact1, mock_db_contact2]
#
#     mock_contact1 = MockContact("John")
#     mock_contact2 = MockContact("Jane")
#     ContactMapper.from_dbmodel.side_effect = [mock_contact1, mock_contact2]
#
#     filename = "contacts.db"
#     address_book = storage.load(filename)
#
#     mock_initialize.assert_called_once_with(db_name=filename)
#     mock_get_all.assert_called_once_with(DBContact)
#     assert isinstance(address_book, AddressBook)
#     assert "John" in address_book.data
#     assert "Jane" in address_book.data
#     assert address_book.data["John"] == mock_contact1
#
#
# def test_save_unsupported_type(storage):
#     """Tests that saving an unsupported data type returns an error string."""
#     with patch.object(storage, 'initialize'):
#         result = storage.save([1, 2, 3], "unsupported.db")
#         assert "Unsupported data type" in result
