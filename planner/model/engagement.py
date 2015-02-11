from sqlalchemy import Column, Float, Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship, validates

from planner.model import Base, ValidationError


class Engagement(Base):
    __tablename__ = 'Engagement'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False)
    revenue = Column(Integer, nullable=False)
    proposal = Column(Text)
    backlog = Column(Text)
    isrnd = Column(Boolean)
    ponumber = Column(Text)

    teamid = Column(Integer, ForeignKey('Team.id'))
    team = relationship("Team")

    clientid = Column(Integer, ForeignKey('Client.id'))
    client = relationship("Client")

    statusid = Column(Integer, ForeignKey('Status.id'))
    status = relationship("Status")

    complexityid = Column(Integer, ForeignKey('Complexity.id'))
    complexity = relationship("Complexity")

    probabilityid = Column(Integer, ForeignKey('Probability.id'))
    probability = relationship("Probability")

    sustainabilityid = Column(Integer, ForeignKey('Sustainability.id'))
    sustainability = relationship("Sustainability")

    alignmentid = Column(Integer, ForeignKey('Alignment.id'))
    alignment = relationship("Alignment")

    expenses = relationship("Expense")


class Status(Base):
    __tablename__ = 'Status'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False, unique=True)


class Alignment(Base):
    __tablename__ = 'Alignment'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Float, nullable=False, unique=True)
    name = Column(Text, nullable=False, unique=True)

    @validates('value')
    def validate_value(self, key, address):
        if address not in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,
                           1.0]:
            raise ValidationError(str(address) + ' is invalid')
        return address


class Sustainability(Base):
    __tablename__ = 'Sustainability'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Float, nullable=False, unique=True)
    name = Column(Text, nullable=False, unique=True)

    @validates('value')
    def validate_value(self, key, address):
        if address not in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,
                           1.0]:
            raise ValidationError(str(address) + ' is invalid')
        return address


class Probability(Base):
    __tablename__ = 'Probability'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Float, nullable=False, unique=True)
    name = Column(Text, nullable=False, unique=True)

    @validates('value')
    def validate_value(self, key, address):
        if address not in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,
                           1.0]:
            raise ValidationError(str(address) + ' is invalid')
        return address


class Complexity(Base):
    __tablename__ = 'Complexity'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Float, nullable=False, unique=True)
    name = Column(Text, nullable=False, unique=True)
    guide_revenue = Column(Integer)

    @validates('value')
    def validate_value(self, key, address):
        if address not in [0.1, 0.5, 1.0, 2.0]:
            raise ValidationError(str(address) + ' is invalid')
        return address
