from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from planner.model import Base


class TransactionFactory(object):
    def __init__(self, path=None, bind=None, expire_on_commit=False,
                 create_all=False):
        if (not bind and not path) or (bind and path):
            raise ValueError
        if not bind:
            bind = create_engine(path)
        if create_all:
            Base.metadata.create_all(bind)
        self.sessionmaker = sessionmaker(expire_on_commit=expire_on_commit,
                                         bind=bind)

    @contextmanager
    def __call__(self, rollback=False):
        try:
            session = self.sessionmaker()
            yield session
            if rollback:
                session.rollback()
            session.commit()
        finally:
            session.close()
