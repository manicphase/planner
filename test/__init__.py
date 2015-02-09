import unittest

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

from planner import create_app
from planner.model import ValidationError
from planner.model.connect import TransactionFactory


class TestConfig:
    DBPATH = "sqlite:///:memory:"
    DBCREATE = True
    DISABLED_FEATURES = []
    TESTING = True


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        self.transaction = TransactionFactory(bind=engine, create_all=True)


class AcceptanceTestCase(BaseTestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()


class ModelTestCase(BaseTestCase):
    def assertHasUniqueName(self, model, **others):
        with self.assertRaises(IntegrityError):
            with self.transaction() as db:
                db.add(model(name=None))

        with self.transaction() as db:
            db.add(model(name="Name", **others))

        with self.assertRaises(IntegrityError):
            with self.transaction() as db:
                db.add(model(name="Name", **others))

    def assertHasValidValue(self, model, low, high, **others):
        with self.assertRaises(ValidationError):
            with self.transaction() as db:
                db.add(model(value=None, **others))

        with self.assertRaises(ValidationError):
            with self.transaction() as db:
                db.add(model(value=low - 0.1, **others))

        with self.assertRaises(ValidationError):
            with self.transaction() as db:
                db.add(model(value=high + 0.1, **others))

        with self.transaction(rollback=True) as db:
            db.add(model(value=low, **others))

        with self.transaction() as db:
            db.add(model(value=high, **others))

    def assertHasUniqueValue(self, model, **others):
        second_name = others['name'][1:]

        with self.transaction() as db:
            db.add(model(value=0.5, **others))

        others['name'] = second_name

        with self.assertRaises(IntegrityError):
            with self.transaction() as db:
                db.add(model(value=0.5, **others))
