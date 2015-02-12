import unittest
import datetime

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.inspection import inspect

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


class TranslationTestCase(BaseTestCase):
    def assertModelsEqual(self, expected, actual):
        if expected is not None and actual is not None:
            if not hasattr(expected, '__table__'):
                for e, a in zip(expected, actual):
                    self.assertModelsEqual(e, a)
            else:
                self.assertEqual(expected.__tablename__, actual.__tablename__)
                for column in expected.__table__.columns:
                    evalue = getattr(expected, column.name)
                    avalue = getattr(actual, column.name)
                    if evalue != avalue:
                        raise AssertionError(
                            '%s MISMATCH %s VS %s' % (column, evalue, avalue))
                for relation in inspect(expected.__class__).relationships:
                    self.assertModelsEqual(getattr(expected, relation.key),
                                           getattr(actual, relation.key))

    def assertDictsEqual(self, expected, actual):
        assert hasattr(expected, 'iteritems')
        assert hasattr(actual, 'iteritems')
        for key, value in expected.iteritems():
            if hasattr(value, 'iteritems'):
                self.assertDictsEqual(value, actual[key])
            elif type(value) in [bool, int, str, unicode, float,
                                 datetime.date]:
                self.assertEqual(value, actual[key])


class AcceptanceTestCase(BaseTestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()


class ModelTestCase(BaseTestCase):
    def assertHasValidUkMobileNumber(self, model, **others):
        self.assertHasValidAttribute(
            model, 'mobileno', '0712345678', valid_set=['07123456789'],
            invalid_set=['ten', '071234567890', '1234567890', '071234567'])

    def assertHasUniqueName(self, model, **others):
        self.assertHasUniqueAttribute(model, 'name', 'Name', **others)

    def assertHasUniqueValue(self, model, value, **others):
        self.assertHasUniqueAttribute(model, 'value', value, **others)

    def assertHasAttribute(self, model, attribute, **others):
        with self.assertRaises((IntegrityError, ValidationError)):
            with self.transaction() as db:
                m = model(**others)
                setattr(m, attribute, None)
                db.add(m)

    def assertHasUniqueAttribute(self, model, attribute, valid, **others):
        self.assertHasAttribute(model, attribute, **others)

        with self.transaction() as db:
            m = model(**others)
            setattr(m, attribute, valid)
            db.add(m)

        with self.assertRaises((IntegrityError, ValidationError)):
            with self.transaction() as db:
                m = model(**others)
                setattr(m, attribute, valid)
                db.add(m)

    def assertHasValidAttribute(
            self, model, attribute, valid, low=None, high=None, unit=None,
            valid_set=None, invalid_set=None, unique=False, lowlen=None,
            highlen=None, **others):
        with self.transaction(rollback=True) as db:
            m = model(**others)
            setattr(m, attribute, valid)
            db.add(m)

        self.assertHasAttribute(model, attribute, **others)

        if unique:
            self.assertHasUniqueAttribute(model, attribute, valid, **others)

        if low or high and not unit:
            raise AssertionError(
                "Unable to perform bounds check as unit not provided")

        if low and unit:
            with self.assertRaises(ValidationError):
                with self.transaction() as db:
                    m = model(**others)
                    setattr(m, attribute, low - unit)
                    db.add(m)

            with self.transaction(rollback=True) as db:
                m = model(**others)
                setattr(m, attribute, low)
                db.add(m)

        if high and unit:
            with self.assertRaises(ValidationError):
                with self.transaction() as db:
                    m = model(**others)
                    setattr(m, attribute, high + unit)
                    db.add(m)

            with self.transaction(rollback=True) as db:
                m = model(**others)
                setattr(m, attribute, high)
                db.add(m)

        if valid_set:
            for valid in valid_set:
                with self.transaction(rollback=True) as db:
                    m = model(**others)
                    setattr(m, attribute, valid)
                    db.add(m)

        if invalid_set:
            for invalid in invalid_set:
                with self.assertRaises(ValidationError):
                    with self.transaction() as db:
                        m = model(**others)
                        setattr(m, attribute, invalid)
                        db.add(m)
        try:
            if lowlen:
                with self.assertRaises(ValidationError):
                    with self.transaction() as db:
                        m = model(**others)
                        setattr(m, attribute, valid[:lowlen - 1])
                        db.add(m)

                with self.transaction(rollback=True) as db:
                    m = model(**others)
                    setattr(m, attribute, valid[:lowlen])
                    db.add(m)

            if highlen:
                invalid = valid
                while len(invalid) < highlen:
                    invalid += valid

                with self.assertRaises(ValidationError):
                    with self.transaction() as db:
                        m = model(**others)
                        setattr(m, attribute, invalid)
                        db.add(m)

                with self.transaction(rollback=True) as db:
                    m = model(**others)
                    setattr(m, attribute, invalid[:highlen])
                    db.add(m)

        except ValueError:
            raise AssertionError("Provided length checking boundary but valid value is not iterable")  # noqa
        except IndexError:
            raise AssertionError("Provided length checking boundary but valid value is not compatible with boundary lengths required")  # noqa
