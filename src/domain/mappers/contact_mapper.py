from .mapper import Mapper
from ..entities.contact import Contact
from ..models.dbcontact import DBContact


class ContactMapper(Mapper):

    @staticmethod
    def to_dbmodel(data: Contact) -> DBContact:
        return DBContact(
            id=data.id,
            name=data.name.value,
            phones=",".join(phone.value for phone in data.phones),
            birthday=data.birthday.value if data.birthday else None,
            email=data.email.value if data.email else None,
            address=data.address.value if data.address else None,
        )

    @staticmethod
    def from_dbmodel(data: DBContact) -> Contact:
        contact = Contact(
            name=data.name,
            contact_id=data.id
        )

        if data.phones:
            for phone in data.phones.split(","):
                contact.add_phone(phone)

        if data.birthday:
            contact.add_birthday(data.birthday)

        if data.email:
            contact.add_email(data.email)

        if data.address:
            contact.add_address(data.address)

        return contact