from sqlalchemy.exc import IntegrityError

from test import ModelTestCase
from planner.model import Client, Engagement


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

    def test_client_should_have_correct_engagements(self):
        expected_name = "TestEngagement"
        with self.transaction() as db:
            db.add(Client(name="TestClient"))
            db.add(Engagement(name=expected_name, revenue=0, clientid=1))

        with self.transaction() as db:
            actual = db.query(Client).first().engagements

        self.assertEquals(1, len(actual))
        self.assertEquals(expected_name, actual[0].name)

    def test_client_engagements_can_be_empty(self):
        with self.transaction() as db:
            db.add(Client(name="TestClient"))

        with self.transaction() as db:
            actual = db.query(Client).first().engagements

        self.assertEquals(0, len(actual))
