from collections import OrderedDict

from sqlalchemy import (
    Column, Float, Integer, Text, ForeignKey, Date, Boolean, Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


class EntityTranslationError(Exception):
    pass


class Api(object):
    __apifields__ = None

    def to_dict(self):
        d = OrderedDict()
        d['entity'] = self.__tablename__
        for field in self.__apifields__:
            d[field] = self.__getattribute__(field)

        return d

    @staticmethod
    def from_dict(cls, data):
        if data['entity'] != cls.__tablename__:
            raise EntityTranslationError

        try:
            r = cls()
            for field in cls.__apifields__:
                r.__setattr__(field, data[field])
        except KeyError:
            raise EntityTranslationError

        return r

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()


Base = declarative_base()

ActualEngagementIteration = Table(
    "ActualEngagementIteration",
    Base.metadata,
    Column('engagementid', Integer, ForeignKey('Engagement.id')),
    Column('iterationid', Integer, ForeignKey('Iteration.id')))
ActualEngagementIteration.__tablename__ = 'ActualEngagementIteration'

EstimatedEngagementIteration = Table(
    "EstimatedEngagementIteration",
    Base.metadata,
    Column('engagementid', Integer, ForeignKey('Engagement.id')),
    Column('iterationid', Integer, ForeignKey('Iteration.id')))
EstimatedEngagementIteration.__tablename__ = 'EstimatedEngagementIteration'

TeamIterationCost = Table(
    "TeamIterationCost",
    Base.metadata,
    Column('teamid', Integer, ForeignKey('Team.id')),
    Column('teamcostid', Integer, ForeignKey('TeamCost.id')))
TeamIterationCost.__tablename__ = 'TeamIterationCost'


class Engagement(Api, Base):
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


class Client(Api, Base):
    __apifields__ = ['name', 'engagements', 'contacts']
    __tablename__ = 'Client'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    engagements = relationship("Engagement", backref="client")
    contacts = relationship("Contact")


class EngagementStatus(Api, Base):
    __apifields__ = ['name', 'engagements']
    __tablename__ = 'EngagementStatus'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    engagements = relationship("Engagement", backref="status")


class EngagementAlignment(Api, Base):
    __apifields__ = ['value', 'name', 'engagements']
    __tablename__ = 'EngagementAlignment'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Float, nullable=False, unique=True)
    name = Column(Text, nullable=False, unique=True)
    engagements = relationship("Engagement", backref='alignment')


class EngagementSustainability(Api, Base):
    __apifields__ = ['value', 'name', 'engagements']
    __tablename__ = 'EngagementSustainability'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Float, nullable=False, unique=True)
    name = Column(Text, nullable=False, unique=True)
    engagements = relationship("Engagement", backref='sustainability')


class EngagementProbability(Api, Base):
    __apifields__ = ['value', 'name', 'engagements']
    __tablename__ = 'EngagementProbability'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Float, nullable=False, unique=True)
    name = Column(Text, nullable=False, unique=True)
    engagements = relationship("Engagement", backref='probability')


class EngagementComplexity(Api, Base):
    __apifields__ = ['value', 'name', 'guide_revenue', 'engagements']
    __tablename__ = 'EngagementComplexity'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Float, nullable=False, unique=True)
    name = Column(Text, nullable=False, unique=True)
    guide_revenue = Column(Integer)
    engagements = relationship("Engagement", backref='complexity')


class Iteration(Api, Base):
    __apifields__ = ['startdate', 'actual', 'estimated']
    __tablename__ = 'Iteration'
    id = Column(Integer, autoincrement=True, primary_key=True)
    startdate = Column(Date, nullable=False)
    actual = relationship("Engagement", secondary="ActualEngagementIteration",
                          backref="actual")
    estimated = relationship("Engagement",
                             secondary="EstimatedEngagementIteration",
                             backref="estimated")


class Team(Api, Base):
    __apifields__ = ['name', 'capacity', 'revenuecap', 'devmax', 'researchmax',
                     'engagements']
    __tablename__ = 'Team'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False)
    capacity = Column(Float, nullable=False)
    revenuecap = Column(Integer, nullable=False)
    devmax = Column(Float, nullable=False)
    researchmax = Column(Float, nullable=False)
    engagements = relationship('Engagement', backref='team')


class Contact(Api, Base):
    __apifields__ = ['forename', 'surname', 'role', 'email', 'landlinenumber',
                     'mobilenumber', 'address', 'client']
    __tablename__ = 'Contact'
    id = Column(Integer, autoincrement=True, primary_key=True)
    forename = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    role = Column(Text)
    email = Column(Text)
    landlinenumber = Column(Text)
    mobilenumber = Column(Text)
    address = Column(Text)
    client = Column(Integer, ForeignKey('Client.id'))


class TeamCost(Api, Base):
    __apifields__ = ['value', 'team', 'iteration']
    __tablename__ = 'TeamCost'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Integer)
    iterationid = Column(Integer, ForeignKey('Iteration.id'))
    iteration = relationship("Iteration")
    team = relationship("Team", secondary="TeamIterationCost", backref="cost")
