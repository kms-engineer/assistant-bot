from dataclasses import dataclass
from src.domain.value_objects.field import Field
from src.domain.validators.address_validator import AddressValidator


@dataclass
class Address(Field):

    def __init__(self, address: str):
        AddressValidator.validate_and_raise(address)
        super().__init__(address.strip())
