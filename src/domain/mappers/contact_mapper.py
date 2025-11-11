from .mapper import Mapper
from ..entities.contact import Contact
from ..models.dbcontact import DBContact
from ..value_objects.name import Name
from ..value_objects.phone import Phone
from ..value_objects.email import Email
from ..value_objects.address import Address
from ..value_objects.birthday import Birthday


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
        name_vo = Name(data.name)
        contact = Contact(name=name_vo, contact_id=data.id)

        if data.phones:
            for phone_str in data.phones.split(","):
                phone_vo = Phone(phone_str)
                contact.add_phone(phone_vo)

        if data.birthday:
            birthday_vo = Birthday(data.birthday)
            contact.add_birthday(birthday_vo)

        if data.email:
            email_vo = Email(data.email)
            contact.add_email(email_vo)

        if data.address:
            address_vo = Address(data.address)
            contact.add_address(address_vo)

        return contact
