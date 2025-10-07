from sqlalchemy import Column, String, Uuid, Integer
from sqlalchemy.orm import relationship

from .dbbase import DBBase

class DBAddress(DBBase):
    __tablename__ = 'addresses'

    id = Column(Uuid, primary_key=True)
    street_name = Column(String, nullable=False)
    street_number = Column(Integer, nullable=False)
    country = Column(String, nullable=True)
    state = Column(String, nullable=True)
    city = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)

    contact = relationship('DBContact', uselist=False, back_populates='address')