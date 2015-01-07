import sqlite3
from datetime import date

from sqlalchemy import create_engine, Column, Integer, Text, Date, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.ext.declarative import declarative_base

from config import LIVEDBPATH, TESTDBPATH


Base = declarative_base()


class Active(Base):
    __tablename__ = 'active'
    id = Column(Integer, primary_key=True)
    engagementid = Column(Integer, ForeignKey('engagement.id'))
    iterationid = Column(Integer, ForeignKey('iteration.id'))


class Estimated(Base):
    __tablename__ = 'estimated'
    id = Column(Integer, primary_key=True)
    engagementid = Column(Integer, ForeignKey('engagement.id'))
    iterationid = Column(Integer, ForeignKey('iteration.id'))


class Engagement(Base):
    __tablename__ = 'engagement'
    id = Column(Integer, primary_key=True)
    teamid = Column(Integer, ForeignKey('team.id'))
    status = Column(Text)
    complexity = Column(Float)
    client = Column(Text)
    project = Column(Text)
    sowlink = Column(Text)
    probability = Column(Float)
    sustainability = Column(Float)
    alignment = Column(Float)
    revenue = Column(Integer)
    type = Column(Text)
    actualiter = relationship(Active, primaryjoin=id == Active.engagementid)
    estimatediter = relationship(Estimated, primaryjoin=id == Estimated.engagementid)
    

class Team(Base):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    capacity = Column(Float)
    revenuecap = Column(Integer)
    annualdevelopmentcapacity = Column(Float)
    annualresearchcapacity = Column(Float)
    engagements = relationship(Engagement, primaryjoin=id == Engagement.teamid)


class Iteration(Base):
    __tablename__ = 'iteration'
    id = Column(Integer, primary_key=True)
    startdate = Column(Date)


LiveSession = sessionmaker(bind=create_engine('sqlite:///' + LIVEDBPATH))
TestSession = sessionmaker(bind=create_engine('sqlite:///' + TESTDBPATH))


def new_test_database():
    _new_database(TESTDBPATH)


def new_live_database():
    _new_database(LIVEDBPATH)


def _new_database(fname):
    conn = sqlite3.connect(fname)
    conn.close()
    engine = create_engine('sqlite:///' + fname)
    Base.metadata.create_all(engine)


def static_live_data():
    session = LiveSession()
    for d in [date(2015, 1, 5), date(2015, 1, 19), date(2015, 2, 2),
              date(2015, 2, 16), date(2015, 3, 2), date(2015, 3, 16),
              date(2015, 3, 30), date(2015, 4, 13), date(2015, 4, 27),
              date(2015, 5, 11), date(2015, 5, 25), date(2015, 6, 8),
              date(2015, 6, 22), date(2015, 7, 6), date(2015, 7, 20),
              date(2015, 8, 3), date(2015, 8, 17), date(2015, 8, 31),
              date(2015, 9, 14), date(2015, 9, 28), date(2015, 10, 12),
              date(2015, 10, 26), date(2015, 11, 9), date(2015, 11, 23),
              date(2015, 12, 7), date(2015, 12, 21)]:
        session.add(Iteration(startdate=d))
        session.add(Team(name=u'TORG', capacity=2.0, revenuecap=36000, annualdevelopmentcapacity=22.0, annualresearchcapacity=4.0))
        session.commit()
        session.close()
