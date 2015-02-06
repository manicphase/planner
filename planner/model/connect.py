import sqlite3
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from planner.model import Base
from planner.config import LIVEDBPATH


LiveSession = sessionmaker(bind=create_engine('sqlite:///' + LIVEDBPATH))


class DbTransactionError(Exception):
    pass


@contextmanager
def transaction(rollback=False, sessionmaker=LiveSession):
    session = sessionmaker()
    try:
        yield session
        if rollback:
            session.rollback()
        session.commit()
    finally:
        session.close()


def new_database(fname):
    conn = sqlite3.connect(fname)
    conn.close()
    engine = create_engine('sqlite:///' + fname)
    Base.metadata.create_all(engine)
