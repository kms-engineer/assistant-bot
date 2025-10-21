from dataclasses import dataclass
from .field import Field
from ..validators.address_validator import AddressValidator


@dataclass
class Address(Field):

    def __init__(self, address: str):
        AddressValidator.validate_and_raise(address)
        super().__init__(address.strip())
