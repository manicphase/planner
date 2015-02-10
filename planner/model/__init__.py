from sqlalchemy import (
    Column, Float, Integer, Text, ForeignKey, Date, Boolean, Table
)
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declarative_base

from planner.api import Api


class ValidationError(Exception):
    pass


Base = declarative_base()

ActualEngagementIteration = Table(
    "ActualEngagementIteration",
    Base.metadata,
    Column('engagementid', Integer, ForeignKey('Engagement.id')),
    Column('iterationid', Integer, ForeignKey('Iteration.id')))

EstimatedEngagementIteration = Table(
    "EstimatedEngagementIteration",
    Base.metadata,
    Column('engagementid', Integer, ForeignKey('Engagement.id')),
    Column('iterationid', Integer, ForeignKey('Iteration.id')))

TeamIterationCost = Table(
    "TeamIterationCost",
    Base.metadata,
    Column('teamid', Integer, ForeignKey('Team.id')),
    Column('teamcostid', Integer, ForeignKey('TeamCost.id')))


class Engagement(Api, Base):
    __apientityname__ = 'Engagement'
    __apifields__ = ['name', 'proposal', 'backlog', 'revenue', 'isrnd',
                     'client', 'status', 'alignment', 'sustainability',
                     'probability', 'complexity', 'actual', 'estimated',
                     'team']
    __tablename__ = 'Engagement'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False)
    proposal = Column(Text)
    backlog = Column(Text)
    revenue = Column(Integer, nullable=False)
    isrnd = Column(Boolean, default=False)

    teamid = Column(Integer, ForeignKey('Team.id'), default=1)
    clientid = Column(Integer, ForeignKey('Client.id'))
    statusid = Column(Integer, ForeignKey('EngagementStatus.id'))
    complexityid = Column(Integer, ForeignKey('EngagementComplexity.id'))
    probabilityid = Column(Integer, ForeignKey('EngagementProbability.id'))
    sustainabilityid = Column(Integer,
                              ForeignKey('EngagementSustainability.id'))
    alignmentid = Column(Integer, ForeignKey('EngagementAlignment.id'))

    client = relationship("Client")
    status = relationship("EngagementStatus")
    alignment = relationship("EngagementAlignment")
    sustainability = relationship("EngagementSustainability")
    probability = relationship("EngagementProbability")
    complexity = relationship("EngagementComplexity")
    actual = relationship("Iteration",
                          secondary="ActualEngagementIteration",
                          lazy="subquery",
                          backref="actual")
    estimated = relationship("Iteration",
                             secondary="EstimatedEngagementIteration",
                             lazy="subquery",
                             backref="estimated")
    team = relationship("Team", backref="engagements")


class Client(Api, Base):
    __apientityname__ = 'Client'
    __apifields__ = ['name', 'contact']
    __tablename__ = 'Client'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False, unique=True)

    contactid = Column(Integer, ForeignKey("Contact.id"))

    contact = relationship("Contact")


class EngagementStatus(Api, Base):
    __apientityname__ = 'EngagementStatus'
    __apifields__ = ['name']
    __tablename__ = 'EngagementStatus'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False, unique=True)


class EngagementAlignment(Api, Base):
    __apientityname__ = 'EngagementAlignment'
    __apifields__ = ['value', 'name']
    __tablename__ = 'EngagementAlignment'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Float, nullable=False, unique=True)
    name = Column(Text, nullable=False, unique=True)

    @validates('value')
    def validate_value(self, key, address):
        if address not in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,
                           1.0]:
            raise ValidationError()
        return address


class EngagementSustainability(Api, Base):
    __apientityname__ = 'EngagementSustainability'
    __apifields__ = ['value', 'name']
    __tablename__ = 'EngagementSustainability'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Float, nullable=False, unique=True)
    name = Column(Text, nullable=False, unique=True)

    @validates('value')
    def validate_value(self, key, address):
        if address not in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,
                           1.0]:
            raise ValidationError()
        return address


class EngagementProbability(Api, Base):
    __apientityname__ = 'EngagementProbability'
    __apifields__ = ['value', 'name']
    __tablename__ = 'EngagementProbability'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Float, nullable=False, unique=True)
    name = Column(Text, nullable=False, unique=True)

    @validates('value')
    def validate_value(self, key, address):
        if address not in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,
                           1.0]:
            raise ValidationError
        return address


class EngagementComplexity(Api, Base):
    __apientityname__ = 'EngagementComplexity'
    __apifields__ = ['value', 'name', 'guide_revenue']
    __tablename__ = 'EngagementComplexity'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Float, nullable=False, unique=True)
    name = Column(Text, nullable=False, unique=True)
    guide_revenue = Column(Integer)

    @validates('value')
    def validate_value(self, key, address):
        if address not in [0.1, 0.5, 1.0, 2.0]:
            raise ValidationError
        return address


class Iteration(Api, Base):
    __apientityname__ = 'Iteration'
    __apifields__ = ['id', 'startdate', 'actual', 'estimated']
    __tablename__ = 'Iteration'
    id = Column(Integer, autoincrement=True, primary_key=True)
    startdate = Column(Date, nullable=False)


class Team(Api, Base):
    __apientityname__ = 'Team'
    __apifields__ = ['name', 'capacity', 'revenuecap', 'devmax', 'researchmax']
    __tablename__ = 'Team'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    capacity = Column(Float, nullable=False)
    revenuecap = Column(Integer, nullable=False)
    devmax = Column(Float, nullable=False)
    researchmax = Column(Float, nullable=False)

    @validates('capacity')
    def validate_capacity(self, key, address):
        if address < self.devmax + self.researchmax:
            raise ValidationError
        return address


class Contact(Api, Base):
    __apientityname__ = "Contact"
    __apifields__ = ['forename', 'surname', 'role', 'email', 'landlinenumber',
                     'mobilenumber', 'postcode', 'streetname', 'streetnumber']
    __tablename__ = 'Contact'
    id = Column(Integer, autoincrement=True, primary_key=True)
    forename = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    role = Column(Text)
    email = Column(Text)
    landlinenumber = Column(Text)
    mobilenumber = Column(Text)
    postcode = Column(Text)
    streetname = Column(Text)
    streetnumber = Column(Text)

    @validates('email')
    def validate_email(self, key, address):
        if '@' not in address:
            raise ValidationError
        return address

    @validates('mobilenumber')
    def validate_mobilenumber(self, key, address):
        if not address.startswith('07') or not len(address) == 10:
            raise ValidationError
        try:
            int(address)
        except TypeError:
            raise ValidationError
        return address


class TeamCost(Api, Base):
    __apientityname__ = 'TeamCost'
    __apifields__ = ['value', 'team', 'iteration']
    __tablename__ = 'TeamCost'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Integer, nullable=False)

    iterationid = Column(Integer, ForeignKey('Iteration.id'), nullable=False)
    teamid = Column(Integer, ForeignKey('Team.id'))

    iteration = relationship("Iteration")
    team = relationship("Team", secondary="TeamIterationCost", backref="cost")

    @validates('value')
    def validate_value(self, key, address):
        if address < 0:
            raise ValidationError
        return address
