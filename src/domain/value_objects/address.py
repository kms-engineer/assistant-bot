from dataclasses import dataclass
from typing import Optional

from ..value_objects.address_objects.city import City
from ..value_objects.address_objects.country import Country
from ..value_objects.address_objects.state import State
from ..value_objects.address_objects.zip_cope import ZipCode
from ..value_objects.address_objects.street_number import StreetNumber
from ..value_objects.address_objects.street_name import StreetName


@dataclass
class Address:
    street_number: StreetNumber
    street_name: StreetName
    city: Optional[City]
    state: Optional[State]
    zip_code: Optional[ZipCode]
    country: Optional[Country]

    def __init__(self, street_number: int, street_name: str, city: str, state: str, zip_code: int, country: str):
        self.street_number = StreetNumber(street_number)
        self.street_name = StreetName(street_name)
        self.city = City(city) if city else None
        self.state = State(state) if state else None
        self.zip_code = ZipCode(zip_code) if zip_code else None
        self.country = Country(country) if country else None


    def __str__(self) -> str:
        return f"{self.street_number} {self.street_name}, {self.city}, {self.state} {self.zip_code}, {self.country}"