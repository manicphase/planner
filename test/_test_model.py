import unittest

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from planner.model import Base, Client
from planner.model.connect import transaction


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        self.sessionmaker = sessionmaker(bind=engine)

    def transaction(self):
        return transaction(sessionmaker=self.sessionmaker)


class TestClient(ModelTestCase):
    def test_client_should_always_have_a_name(self):
        with self.assertRaises(IntegrityError):
            with self.transaction() as db:
                db.add(Client(name=None))

    def test_clients_name_should_be_unique(self):
        with self.transaction() as db:
            db.add(Client(name="TestClient"))

        with self.assertRaises(IntegrityError):
            with self.transaction() as db:
                db.add(Client(name="TestClient"))

    def test_client_should_have_engagements(self):
        pass

    def test_client_engagements_can_be_empty(self):
        with self.transaction() as db:
            db.add(Client(name="TestClient"))

        with self.transaction() as db:
            actual = db.query(Client).first().engagements

        self.assertEquals(0, len(actual))

    def test_client_to_dict_should_be_accurate(self):
        pass

    def test_client_to_dict_should_call_engagements_to_dict(self):
        pass

    def test_client_from_dict_should_be_accurate(self):
        pass

    def test_client_from_dict_should_call_engagements_from_dict(self):
        pass
