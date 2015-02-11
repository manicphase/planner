from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


class ValidationError(Exception):
    pass


Base = declarative_base()


class EngagementIteration(Base):
    __tablename__ = 'EngagementIteration'
    engagementid = Column(Integer, ForeignKey('Engagement.id'),
                          primary_key=True)
    iterationid = Column(Integer, ForeignKey('Iteration.id'), primary_key=True)

    engagement = relationship("Engagement")
    iteration = relationship("Iteration")


class EstimatedEngagementIteration(Base):
    __tablename__ = 'EstimatedEngagementIteration'
    engagementid = Column(Integer, ForeignKey('Engagement.id'),
                          primary_key=True)
    iterationid = Column(Integer, ForeignKey('Iteration.id'),
                         primary_key=True)

    engagement = relationship("Engagement")
    iteration = relationship("Iteration")
