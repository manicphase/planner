from collections import OrderedDict

from sqlalchemy import (
    Column, Float, Integer, Text, ForeignKey, Date, Boolean, Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


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


class Api(object):
    def to_dict(self):
        raise NotImplementedError

    @staticmethod
    def from_dict(data):
        raise NotImplementedError


class EntityTranslationError(Exception):
    pass


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
    __tablename__ = 'Client'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    engagements = relationship("Engagement", backref="client")
    contacts = relationship("Contact")

    def to_dict(self):
        d = OrderedDict()
        d['entity'] = Client.__tablename__
        d['name'] = self.name
        d['engagements'] = [e.to_dict() for e in self.engagements]
        return d

    @staticmethod
    def from_dict(data):
        if data['entity'] != Client.__tablename__:
            raise EntityTranslationError

        try:
            client = Client(name=data['name'], engagements=data['engagements'])
        except KeyError:
            raise EntityTranslationError

        return client

    def __eq__(self, other):
        try:
            return self.to_dict() == other.to_dict()
        except:
            return False


class EngagementStatus(Api, Base):
    __tablename__ = 'EngagementStatus'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    engagements = relationship("Engagement", backref="status")


class EngagementAlignment(Api, Base):
    __tablename__ = 'EngagementAlignment'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Float, nullable=False, unique=True)
    name = Column(Text, nullable=False, unique=True)
    engagements = relationship("Engagement", backref='alignment')


class EngagementSustainability(Api, Base):
    __tablename__ = 'EngagementSustainability'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Float, nullable=False, unique=True)
    name = Column(Text, nullable=False, unique=True)
    engagements = relationship("Engagement", backref='sustainability')


class EngagementProbability(Api, Base):
    __tablename__ = 'EngagementProbability'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Float, nullable=False, unique=True)
    name = Column(Text, nullable=False, unique=True)
    engagements = relationship("Engagement", backref='probability')


class EngagementComplexity(Api, Base):
    __tablename__ = 'EngagementComplexity'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Float, nullable=False, unique=True)
    name = Column(Text, nullable=False, unique=True)
    guide_revenue = Column(Integer)
    engagements = relationship("Engagement", backref='complexity')


class Iteration(Api, Base):
    __tablename__ = 'Iteration'
    id = Column(Integer, autoincrement=True, primary_key=True)
    startdate = Column(Date, nullable=False)
    actual = relationship("Engagement", secondary="ActualEngagementIteration",
                          backref="actual")
    estimated = relationship("Engagement",
                             secondary="EstimatedEngagementIteration",
                             backref="estimated")


class Team(Api, Base):
    __tablename__ = 'Team'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False)
    capacity = Column(Float, nullable=False)
    revenuecap = Column(Integer, nullable=False)
    devmax = Column(Float, nullable=False)
    researchmax = Column(Float, nullable=False)
    engagements = relationship('Engagement', backref='team')


class Contact(Api, Base):
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
    __tablename__ = 'TeamCost'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Integer)
    iterationid = Column(Integer, ForeignKey('Iteration.id'))
    team = relationship("Team", secondary="TeamIterationCost", backref="cost")
