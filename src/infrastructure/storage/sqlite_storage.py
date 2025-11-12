from pathlib import Path
from typing import Any, Optional, List, Type, TypeVar

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

from .storage_type import StorageType
from ..persistence.data_path_resolver import DataPathResolver
from ..storage.storage import Storage
from ...domain.address_book import AddressBook
from ...domain.notebook import Notebook
from ...domain.mappers.contact_mapper import ContactMapper
from ...domain.mappers.note_mapper import NoteMapper
from ...domain.models.dbcontact import DBContact
from ...domain.models.dbnote import DBNote

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

    def __init__(self, base: Type[DeclarativeBase], data_dir: Path | None = None):
        self.resolver = DataPathResolver(data_dir) if data_dir else DataPathResolver()
        self._is_initialized = False
        self._base_class = base
        self._session_factory = None
        self._engine : Engine | None = None

    def _create_session(self) -> Session:
        if not self._is_initialized:
            raise RuntimeError(
                "SQLiteStorage is not initialized. Call 'initialize' method first."
            )
        if self._session_factory is None:
            raise RuntimeError(
                "Session factory is not set. Ensure 'initialize' method has been called."
            )
        return self._session_factory()

    def initialize(self, db_name: str) -> None:
        db_path = self.resolver.get_full_path(db_name)
        print(f"Initializing SQLite database at {db_path}")
        self._engine = create_engine(
            f"sqlite:///{db_path}", echo=False, future=True
        )
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
            # Clear existing contacts and save new ones
            self._clear_and_save(
                DBContact, data.data.values(), ContactMapper.to_dbmodel
            )
            return filename
        elif isinstance(data, Notebook):
            # Clear existing notes and save new ones
            self._clear_and_save(DBNote, data.data.values(), NoteMapper.to_dbmodel)
            return filename

        return (
            "Unsupported data type for save operation. Supported: AddressBook, Notebook"
        )

    def _clear_and_save(self, model_class, entities, mapper_func):
        with self._create_session() as session:
            try:
                # Get existing IDs from database
                existing_ids = {
                    record.id for record in session.query(model_class.id).all()
                }

                # Get IDs from entities to save
                entity_ids = set()
                entities_list = list(entities)

                # Save/update all entities
                for entity in entities_list:
                    db_model = mapper_func(entity)
                    entity_ids.add(db_model.id)
                    merged_entity = session.merge(db_model)
                    session.add(merged_entity)

                # Delete records that are no longer in the collection
                ids_to_delete = existing_ids - entity_ids
                if ids_to_delete:
                    session.query(model_class).filter(
                        model_class.id.in_(ids_to_delete)
                    ).delete(synchronize_session=False)

                session.commit()
            except Exception as e:
                log.error(f"Failed to clear and save: {e}")
                session.rollback()
                raise

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
            log.error(f"Failed to load address book: {e}")
            return None

    def load_notes(self, filename: str, **kwargs) -> Optional[Notebook]:
        if not self._is_initialized:
            self.initialize(db_name=filename)
        try:
            db_notes = self.get_all(DBNote)
            notebook = Notebook()
            for db_note in db_notes:
                note = NoteMapper.from_dbmodel(db_note)
                notebook[note.id] = note
            return notebook
        except Exception as e:
            log.error(f"Failed to load notebook: {e}")
            return None
