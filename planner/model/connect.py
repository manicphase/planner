import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from planner.model import Base
from planner.config import LIVEDBPATH


LiveSession = sessionmaker(bind=create_engine('sqlite:///' + LIVEDBPATH))


def new_database(fname):
    conn = sqlite3.connect(fname)
    conn.close()
    engine = create_engine('sqlite:///' + fname)
    Base.metadata.create_all(engine)

