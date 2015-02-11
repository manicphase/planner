from sqlalchemy import Column, Float, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, validates

from planner.model import Base, ValidationError


class Team(Base):
    __tablename__ = 'Team'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    capacity = Column(Float, nullable=False)
    revenuecap = Column(Integer, nullable=False)
    devmax = Column(Float, nullable=False)
    researchmax = Column(Float, nullable=False)

    members = relationship("TeamMember")

    @validates('capacity')
    def validate_capacity(self, key, address):
        if address < self.devmax + self.researchmax:
            raise ValidationError(str(address) + ' is invalid')
        return address


class TeamMember(Base):
    __tablename__ = 'TeamMember'
    id = Column(Integer, autoincrement=True, primary_key=True)
    forename = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    gmail = Column(Text, nullable=False)
    mobileno = Column(Text, nullable=False)
    twitter = Column(Text, nullable=False)
    github = Column(Text, nullable=False)
    picture = Column(Text, nullable=False)
    bio = Column(Text, nullable=False)

    teamid = Column(Integer, ForeignKey("Team.id"))

    costs = Column(Integer, ForeignKey("Cost.id"))

    @validates('title')
    def validate_title(self, key, address):
        if address not in ['Mr', 'Miss', 'Dr', 'Mrs']:
            raise ValidationError(
                    str(address) + " is not an appropriate title")
        return address

    @validates('gmail')
    def validate_gmail(self, key, address):
        if '@' not in address:
            raise ValidationError(address + ' is invalid')

        return address

    @validates('mobileno')
    def validate_mobileno(self, key, address):
        if address is not None:
            if address.startswith('07') and len(address) in [10, 11]:
                try:
                    int(address[1:])
                    return address
                except TypeError:
                    pass
        raise ValidationError(str(address) + " is invalid")


class Cost(Base):
    __tablename__ = 'Cost'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Integer, nullable=False)

    costtypeid = Column(Integer, ForeignKey("CostType.id"))
    teammemberid = Column(Integer, ForeignKey("Cost.id"))

    teammember = Column(Integer, ForeignKey("TeamMember.id"))
    type = relationship("CostType")

    @validates('value')
    def validate_value(self, key, address):
        if address < 0:
            raise ValidationError(str(address) + ' is invalid')
        return address


class CostType(Base):
    __tablename__ = 'CostType'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
