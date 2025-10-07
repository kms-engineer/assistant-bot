from sqlalchemy import Column, String

from .dbbase import DBBase


class DBContact(DBBase):
    __tablename__ = 'contacts'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    birthday = Column(String, nullable=True)
    # Comma-separated phone numbers
    phones = Column(String, nullable=True)
    email = Column(String, nullable=True)
    address = Column(String, nullable=True)
