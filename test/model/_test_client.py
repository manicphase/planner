from test import ModelTestCase
from planner.model import ValidationError
from planner.model.client import Client, Contact


class TestClient(ModelTestCase):
    def test_client_should_always_have_a_unique_name(self):
        self.assertHasUniqueName(Client)

    def test_client_should_have_correct_contact(self):
        with self.transaction() as db:
            db.add(Client(name="Name",
                          contact=Contact(forename="Mc", surname="Test")))

        with self.transaction() as db:
            actual = db.query(Client).first()

        self.assertEquals("Mc", actual.contact.forename)
        self.assertEquals("Test", actual.contact.surname)


class TestContact(ModelTestCase):
    def test_contact_email_should_contain_at_symbol(self):
        with self.assertRaises(ValidationError):
            with self.transaction() as db:
                db.add(Contact(forename="Mc", surname="Test", email="no.com"))

    def test_contact_mobilenumber_should_be_valid_uk_mobile(self):
        self.assertHasValidUkMobileNumber(Contact, forename="", surname="")
