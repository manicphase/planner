from sqlalchemy import (
    Column, Float, Integer, Text, ForeignKey, Date, Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class ActualEngagementIteration(Base):
    __tablename__ = 'ActualEngagementIteration'
    id = Column(Integer, primary_key=True, autoincrement=True)
    engagementid = Column(Integer, ForeignKey('Engagement.id'))
    iterationid = Column(Integer, ForeignKey('Iteration.id'))


class EstimatedEngagementIteration(Base):
    __tablename__ = 'EstimatedEngagementIteration'
    id = Column(Integer, primary_key=True, autoincrement=True)
    engagementid = Column(Integer, ForeignKey('Engagement.id'))
    iterationid = Column(Integer, ForeignKey('Iteration.id'))


class Engagement(Base):
    __tablename__ = 'Engagement'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False)
    proposal = Column(Text, nullable=False)
    backlog = Column(Text, nullable=False)
    revenue = Column(Integer, nullable=False)
    isrnd = Column(Boolean, nullable=False)

    teamid = Column(Integer, ForeignKey('Team.id'), default=1)
    clientid = Column(Integer, ForeignKey('Client.id'))
    statusid = Column(Integer, ForeignKey('EngagementStatus.id'))
    complexityid = Column(Integer, ForeignKey('EngagementComplexity.id'))
    probabilityid = Column(Integer, ForeignKey('EngagementProbability.id'))
    sustainabilityid = Column(Integer,
                              ForeignKey('EngagementSustainability.id'))
    alignmentid = Column(Integer, ForeignKey('EngagementAlignment.id'))


class Client(Base):
    __tablename__ = 'Client'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    engagements = relationship("Engagement", backref="client")


class EngagementStatus(Base):
    __tablename__ = 'EngagementStatus'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    engagements = relationship("Engagement", backref="status")


class EngagementAlignment(Base):
    __tablename__ = 'EngagementAlignment'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Float, nullable=False, unique=True)
    name = Column(Text, nullable=False, unique=True)
    engagements = relationship("Engagement", backref='alignment')


class EngagementSustainability(Base):
    __tablename__ = 'EngagementSustainability'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Float, nullable=False, unique=True)
    name = Column(Text, nullable=False, unique=True)
    engagements = relationship("Engagement", backref='sustainability')


class EngagementProbability(Base):
    __tablename__ = 'EngagementProbability'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Float, nullable=False, unique=True)
    engagements = relationship("Engagement", backref='probability')


class EngagementComplexity(Base):
    __tablename__ = 'EngagementComplexity'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Float, nullable=False, unique=True)
    name = Column(Text, nullable=False, unique=True)
    guide_revenue = Column(Integer)
    engagements = relationship("Engagement", backref='complexity')


class Iteration(Base):
    __tablename__ = 'Iteration'
    id = Column(Integer, autoincrement=True, primary_key=True)
    startdate = Column(Date, nullable=False)
    actual = relationship("Engagement", secondary="ActualEngagementIteration",
                          backref="actual")
    estimated = relationship("Engagement",
                             secondary="EstimatedEngagementIteration",
                             backref="estimated")


class Team(Base):
    __tablename__ = 'Team'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False)
    capacity = Column(Float, nullable=False)
    revenuecap = Column(Integer, nullable=False)
    devmax = Column(Float, nullable=False)
    researchmax = Column(Float, nullable=False)
    engagements = relationship('Engagement', backref='team')
    cost = relationship('TeamCost', backref='team')


class TeamCost(Base):
    __tablename__ = 'TeamCost'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Integer)
    iterationid = Column(Integer, ForeignKey('Iteration.id'))
