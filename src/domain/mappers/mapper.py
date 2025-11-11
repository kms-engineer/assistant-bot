from abc import ABC, abstractmethod

from ..entities.entity import Entity
from ..models.dbbase import DBBase


class Mapper(ABC):

    @abstractmethod
    def to_dbmodel(self, data: Entity) -> DBBase:
        pass

    @abstractmethod
    def from_dbmodel(self, data: DBBase) -> Entity:
        pass
