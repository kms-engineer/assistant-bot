from sqlalchemy import Column, String

from .dbbase import DBBase


class DBNote(DBBase):
    __tablename__ = 'notes'

    id = Column(String, primary_key=True)
    text = Column(String, nullable=False)
    # Comma-separated tags
    tags = Column(String, nullable=True)
