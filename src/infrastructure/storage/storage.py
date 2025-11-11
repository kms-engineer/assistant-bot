from abc import ABC, abstractmethod
from typing import Any, Optional

from .storage_type import StorageType


class Storage(ABC):
    @abstractmethod
    def save(self, data: Any, filename: str, **kwargs) -> str:
        pass

    @abstractmethod
    def load(self, filename: str, **kwargs) -> Optional[Any]:
        pass

    @property
    @abstractmethod
    def file_extension(self) -> str:
        pass

    @property
    @abstractmethod
    def storage_type(self) -> StorageType:
        pass
