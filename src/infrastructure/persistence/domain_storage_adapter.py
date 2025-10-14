import json
from typing import Any, Optional
from ..storage.storage import Storage
from ..serialization.json_serializer import JsonSerializer
from ..storage.storage_type import StorageType
from ...application.exceptions.base import StorageException
from ...domain.entities.note import Note
from ...domain.notebook import Notebook


class DomainStorageAdapter:

    def __init__(self, storage: Storage, serializer: JsonSerializer = None):
        self.storage = storage
        self.serializer = serializer if serializer else JsonSerializer()
        self.resolver = getattr(storage, 'resolver', None)

    @property
    def file_extension(self) -> str:
        return self.storage.file_extension

    def ensure_suffix(self, filename: str) -> str:
        if not self.resolver:
            return filename

        if self.storage.file_extension == '.json':
            return self.resolver.ensure_json_suffix(filename)
        elif self.storage.file_extension == '.pkl':
            return self.resolver.ensure_pkl_suffix(filename)
        return filename

    def save_contacts(self, address_book, filename: str, **kwargs) -> str:
        if self.storage.storage_type == StorageType.PICKLE \
                or self.storage.storage_type == StorageType.SQLITE:
            data = address_book
        elif self.storage.storage_type == StorageType.JSON:
            data = [
                self.serializer.contact_to_dict(contact)
                for contact in address_book.data.values()
            ]
        else:
            raise StorageException("Unsupported storage type for saving contacts")

        saved_filename = self.storage.save(data, filename, **kwargs)
        return self.ensure_suffix(saved_filename)

    def load_contacts(self, filename: str, **kwargs):
        from ...domain.address_book import AddressBook

        loaded = self.storage.load(filename, **kwargs)
        normalized_filename = self.ensure_suffix(filename)

        if loaded is None:
            return None, normalized_filename
        elif hasattr(loaded, 'data') and hasattr(loaded, 'add_record'):
            return loaded, normalized_filename
        elif isinstance(loaded, list):
            address_book = AddressBook()
            seen_ids = set()
            for contact_dict in loaded:
                contact = self.serializer.dict_to_contact(contact_dict)
                if contact.id in seen_ids:
                    continue
                seen_ids.add(contact.id)
                try:
                    address_book.add_record(contact)
                except KeyError:
                    continue
            return address_book, normalized_filename
        else:
            return None, normalized_filename

    def save_notes(self, notes: dict[str, Note], filename: str, **kwargs) -> str:
        if self.storage.storage_type == StorageType.PICKLE:
            data = notes
        elif self.storage.storage_type == StorageType.JSON:
            data = [
                self.serializer.note_to_dict(note)
                for note in notes.values()
            ]

        elif self.storage.storage_type == StorageType.SQLITE:
            raise StorageException("Not implemented type for saving notes")
        else:
            raise StorageException("Unsupported storage type for saving notes")

        saved_filename = self.storage.save(data, filename, **kwargs)
        return self.ensure_suffix(saved_filename)

    def load_notes(self, filename: str, **kwargs):
        loaded = self.storage.load(filename, **kwargs)
        normalized_filename = self.ensure_suffix(filename)
        notes_dict = {}

        if isinstance(loaded, dict):
            notes_dict = loaded
        elif isinstance(loaded, list):
            for note_dict in loaded:
                note = self.serializer.dict_to_note(note_dict)
                if note.id not in notes_dict:
                    notes_dict[note.id] = note

        return notes_dict, normalized_filename


