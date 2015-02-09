from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from planner.model import Base
from planner.config import LiveConfig


LiveSession = sessionmaker(bind=create_engine(LiveConfig.LIVEDBPATH))


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


def new_database():
    engine = create_engine(LiveConfig.LIVEDBPATH)
    Base.metadata.create_all(engine)
