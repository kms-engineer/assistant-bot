from sqlalchemy import Column, String, Integer, Uuid
from sqlalchemy.orm import relationship

from .dbbase import DBBase

from .dbnote import note_tags_table

class DBTag(DBBase):
    __tablename__ = 'tags'

    id = Column(String, primary_key=True)
    value = Column(String, nullable=False)
    notes = relationship('DBNote', note_tags_table, back_populates='tags')
