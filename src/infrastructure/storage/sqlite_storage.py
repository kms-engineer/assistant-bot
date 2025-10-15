from pathlib import Path
from typing import Any, Optional, List, Type, TypeVar

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

from .storage_type import StorageType
from ..persistence.data_path_resolver import DataPathResolver
from ..storage.storage import Storage
from ...domain.address_book import AddressBook
from ...domain.mappers.contact_mapper import ContactMapper
from ...domain.models.dbcontact import DBContact

T = TypeVar("T")

from ..logging.logger import setup_logger
log = setup_logger()

# import logging
# log = logging.getLogger(__name__)


class SQLiteStorage(Storage):

    @property
    def file_extension(self) -> str:
        return ".db"

    @property
    def storage_type(self) -> StorageType:
        return StorageType.SQLITE

    def __init__(self, base: Type[DeclarativeBase], data_dir: Path = None):
        self.resolver = DataPathResolver(data_dir) if data_dir else DataPathResolver()
        self._is_initialized = False
        self._base_class = base
        self._session_factory = None
        self._engine = None


    def _create_session(self) -> Session:
        if not self._is_initialized:
            raise RuntimeError("SQLiteStorage is not initialized. Call 'initialize' method first.")
        if self._session_factory is None:
            raise RuntimeError("Session factory is not set. Ensure 'initialize' method has been called.")
        return self._session_factory()

    def initialize(self, db_name: str) -> None:
        db_path = self.resolver.get_full_path(db_name)
        print(f"Initializing SQLite database at {db_path}")
        self._engine: Engine = create_engine(f"sqlite:///{db_path}", echo=False, future=True)
        self._session_factory = sessionmaker(bind=self._engine, expire_on_commit=False)
        self._is_initialized = True
        self._base_class.metadata.create_all(self._engine)

    def save_entity(self, entity: T) -> T:
        log.debug(f"Saving entity of type {type(entity).__name__}")
        with self._create_session() as session:
            try:
                merged_entity = session.merge(entity)
                session.commit()
                session.expunge(merged_entity)
                return merged_entity
            except Exception as e:
                log.error(f"Failed to save entity: {e}")
                session.rollback()
                raise

    def get_entity(self, model_class: Type[T], primary_key: Any) -> Optional[T]:
        log.debug(f"Getting {model_class.__name__} with pk={primary_key}")
        with self._create_session() as session:
            entity = session.get(model_class, primary_key)
            if entity:
                session.expunge(entity)  # Від'єднуємо від сесії
            return entity

    def get_all(self, model_class: Type[T]) -> List[T]:
        log.debug(f"Getting all entities for {model_class.__name__}")
        with self._create_session() as session:
            entities = session.query(model_class).all()
            session.expunge_all()  # Від'єднуємо всі об'єкти
            return entities

    def delete_entity(self, entity: T) -> None:
        log.debug(f"Deleting entity of type {type(entity).__name__}")
        with self._create_session() as session:
            try:
                # Приєднуємо об'єкт до нової сесії, щоб його можна було видалити
                session.delete(session.merge(entity))
                session.commit()
            except Exception as e:
                log.error(f"Failed to delete entity: {e}")
                session.rollback()
                raise


    def save(self, data: Any, filename: str, **kwargs) -> str:
        self.initialize(db_name=filename)

        if isinstance(data, AddressBook):
            for contact in data.data.values():
                db_model = ContactMapper.to_dbmodel(contact)
                self.save_entity(db_model)
            return filename

        return "Unsupported data type for save operation. Supported: AddressBook, Notebook"


    def load(self, filename: str, **kwargs) -> Optional[Any]:
        if not self._is_initialized:
            self.initialize(db_name=filename)
        try:
            db_contacts = self.get_all(DBContact)
            address_book = AddressBook()
            for db_contact in db_contacts:
                contact = ContactMapper.from_dbmodel(db_contact)
                address_book.add_record(contact)
            return address_book
        except Exception as e:
            log.error(f"Failed to load data: {e}")
            return None
