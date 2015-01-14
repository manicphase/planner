from sqlalchemy import Table, Column, Float, Integer, Text, ForeignKey, Date, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

EstimatedEngagementIteration = Table('EstimatedEngagementIteration', Base.metadata,
        Column('engagementid', Integer, ForeignKey('Engagement.id')),
        Column('iterationid', Integer, ForeignKey('Iteration.id')))

ActualEngagementIteration = Table('ActualEngagementIteration', Base.metadata,
        Column('engagementid', Integer, ForeignKey('Engagement.id')),
        Column('iterationid', Integer, ForeignKey('Iteration.id')))

FreeEngagementIteration = Table('FreeEngagementIteration', Base.metadata,
        Column('engagementid', Integer, ForeignKey('Engagement.id')),
        Column('iterationid', Integer, ForeignKey('Iteration.id')))


class Engagement(Base):
    __tablename__ = 'Engagement'
    id = Column(Integer, autoincrement=True, primary_key=True)
    teamid = Column(Integer, ForeignKey('Team.id'), default=1)
    name = Column(Text, nullable=False)
    complexity = Column(Enum('0.1', '0.5', '1.0', '2.0', name='engagementcomplexity'), nullable=False)
    client = Column(Text, nullable=False)
    sowlink = Column(Text, nullable=False)
    probability = Column(Enum('0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0', name='engagementprobability'), nullable=False)
    sustainability = Column(Enum('0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0', name='engagementsustainability'), nullable=False)
    alignment = Column(Enum('0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0', name='engagementalignment'), nullable=False)
    revenue = Column(Integer, nullable=False)
    isrnd = Column(Boolean, nullable=False)
    status = Column(Enum('Complete', 'Sold', 'Negotiation', 'Approach', 'Lost', name='engagementstatus'), nullable=False)

    def probable_complexity(self):
        return float(self.complexity) * float(self.probability)


class Iteration(Base):
    __tablename__ = 'Iteration'
    id = Column(Integer, autoincrement=True, primary_key=True)
    startdate = Column(Date, nullable=False)
    actual = relationship("Engagement", secondary="ActualEngagementIteration", backref="actual")
    estimated = relationship("Engagement", secondary="EstimatedEngagementIteration", backref="estimated") 


class Team(Base):
    __tablename__ = 'Team'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False)
    capacity = Column(Float, nullable=False)
    revenuecap = Column(Integer, nullable=False)
    devmax = Column(Float, nullable=False)
    researchmax = Column(Float, nullable=False)
    cost = Column(Integer, nullable=False)
    engagements = relationship('Engagement', backref='team')

