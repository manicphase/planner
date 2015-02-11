from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, validates

from planner.model import Base, ValidationError


class Client(Base):
    __tablename__ = 'Client'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False, unique=True)

    contactid = Column(Integer, ForeignKey("Contact.id"))

    contact = relationship("Contact", lazy="subquery")


class Contact(Base):
    __tablename__ = 'Contact'
    id = Column(Integer, autoincrement=True, primary_key=True)
    forename = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    role = Column(Text)
    email = Column(Text)
    landlineno = Column(Text)
    mobileno = Column(Text)
    postcode = Column(Text)
    streetname = Column(Text)
    streetnumber = Column(Text)

    @validates('email')
    def validate_email(self, key, address):
        if '@' not in address:
            raise ValidationError
        return address

    @validates('mobileno')
    def validate_mobilenumber(self, key, address):
        if address is not None:
            if address.startswith('07') and len(address) in [10, 11]:
                try:
                    int(address[1:])
                    return address
                except TypeError:
                    pass
        raise ValidationError(str(address) + " is invalid")
