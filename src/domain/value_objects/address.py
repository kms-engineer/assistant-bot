from dataclasses import dataclass
from .field import Field
from ..validators.address_validator import AddressValidator


@dataclass
class Address(Field):

    def __init__(self, address: str):
        if not AddressValidator.validate(address):
            raise ValueError("Invalid address format")
        super().__init__(address.strip())
