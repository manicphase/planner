import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from planner.model import Base, ValidationError
from planner.model.connect import transaction


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        self.sessionmaker = sessionmaker(expire_on_commit=False, bind=engine)

    def transaction(self, rollback=False):
        return transaction(rollback=rollback, sessionmaker=self.sessionmaker)

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
