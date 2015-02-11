from sqlalchemy import Column, Integer, Text, ForeignKey, Date
from sqlalchemy.orm import relationship, validates

from planner.model import Base, ValidationError


class Iteration(Base):
    __tablename__ = 'Iteration'
    id = Column(Integer, autoincrement=True, primary_key=True)
    startdate = Column(Date, nullable=False)

    engagements = relationship("EngagementIteration")


class EstimatedIteration(Base):
    __tablename__ = 'EstimatedIteration'
    id = Column(Integer, autoincrement=True, primary_key=True)
    startdate = Column(Date, nullable=False)

    engagements = relationship("EstimatedEngagementIteration")


class Expense(Base):
    __tablename__ = 'Expense'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Integer, nullable=False)
    trackerid = Column(Text, nullable=False)

    engagementid = Column(Integer, ForeignKey('Engagement.id'), nullable=False)
    iterationid = Column(Integer, ForeignKey('Iteration.id'), nullable=False)

    @validates('value')
    def validate_value(self, key, address):
        if address < 0:
            raise ValidationError
        return address
