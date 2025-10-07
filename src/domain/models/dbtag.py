from sqlalchemy import Column, String, Integer, Uuid
from sqlalchemy.orm import relationship

from .dbbase import DBBase

from .dbnote import note_tags_table

class DBTag(DBBase):
    __tablename__ = 'tags'

    id = Column(Uuid, primary_key=True)
    value = Column(String, nullable=False)
    notes = relationship('DbNote', note_tags_table, back_populates='tags')