from sqlalchemy import Column, String

from src.domain.models.dbbase import DBBase


class DBNote(DBBase):
    __tablename__ = "notes"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    # Comma-separated tags
    tags = Column(String, nullable=True)
