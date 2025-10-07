from sqlalchemy import Column, String, Uuid
from sqlalchemy.orm import relationship

from .dbbase import DBBase

class DBContact(DBBase):
    __tablename__ = 'contacts'

    id = Column(Uuid, primary_key=True)
    name = Column(String, nullable=False)
    birthday = Column(String, nullable=True)
    email = Column(String, nullable=True)
    address = relationship('DBAddress', useList=False, back_populates='contact')