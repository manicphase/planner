import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from planner.model import Base
from planner.model.connect import transaction


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        self.sessionmaker = sessionmaker(expire_on_commit=False, bind=engine)

    def transaction(self):
        return transaction(sessionmaker=self.sessionmaker)
