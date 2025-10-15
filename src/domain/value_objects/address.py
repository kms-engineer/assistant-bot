from dataclasses import dataclass
from .field import Field
from ..validators.address_validator import AddressValidator


@dataclass
class Address(Field):

    def __init__(self, address: str):
        validation_result = AddressValidator.validate(address)
        if validation_result is not True:
            raise ValueError(str(validation_result))
        super().__init__(address.strip())
