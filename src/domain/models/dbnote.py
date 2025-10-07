from typing import List

from sqlalchemy import Column, String, Uuid, Table, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from .dbbase import DBBase

note_tags_table = Table(
    'note_tags',
    DBBase.metadata,
    Column('note_id', Uuid, ForeignKey('notes.id'), primary_key=True),
    Column('tag_id', Uuid, ForeignKey('tags.id'), primary_key=True)
)

class DBNote(DBBase):
    __tablename__ = 'notes'

    id = Column(Uuid, primary_key=True)
    text = Column(String, nullable=False)
    tags = relationship('DBTag', secondary=note_tags_table, back_populates='notes')