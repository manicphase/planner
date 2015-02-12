from test import TranslationTestCase
from planner.model.translate import to_model, to_dict
from planner.model import engagement as e
from planner.model import client as c


class TestTranslate(TranslationTestCase):
    def test_model_should_jsonify_simple_columns(self):
        expected = {'entity': 'ExpenseType', 'name': 'Test'}

        actual = to_dict(e.ExpenseType(name="Test"))

        self.assertDictsEqual(expected, actual)

    def test_model_should_jsonify_model_columns(self):
        expected = {'entity': 'Expense', 'value': 1, 'paid': False,
                    'trackerid': '1', 'type': {'entity': 'ExpenseType',
                                               'name': 'Test'}}

        actual = to_dict(e.Expense(value=1, paid=False, trackerid='1',
                         type=e.ExpenseType(name="Test")))

        self.assertDictsEqual(expected, actual)

    def test_model_should_jsonify_iterable_model_columns(self):
        expected = {'entity': 'Client', 'name': 'SomeCo',
                    'contacts': [{'entity': 'Contact', 'forename': 'Bossy',
                                  'surname': 'McBoss'},
                                 {'entity': 'Contact', 'forename': 'Technie',
                                  'surname': 'Technicsen'}]}

        actual = to_dict(
            c.Client(name='SomeCo',
                     contacts=[c.Contact(forename='Bossy', surname='McBoss'),
                               c.Contact(forename='Technie',
                                         surname='Technicsen')]))

        self.assertDictsEqual(expected, actual)

    def test_to_model_should_objectify_simple_columns(self):
        expected = e.ExpenseType(name="Test")

        actual = to_model({'entity': 'ExpenseType', 'name': 'Test'}, e)

        self.assertModelsEqual(expected, actual)

    def test_to_model_should_objectify_model_columns(self):
        travel = e.ExpenseType(name="Travel")
        expected = e.Expense(value=1, trackerid='1', paid=False, type=travel)

        actual = to_model(
            {'entity': 'Expense', 'value': 1, 'paid': False, 'trackerid': '1',
             'type': {'entity': 'ExpenseType', 'name': 'Travel'}}, e)

        self.assertModelsEqual(expected, actual)

    def test_to_model_should_objectify_iterable_model_columns(self):
        boss = c.Contact(forename='Bossy', surname='McBoss')
        techie = c.Contact(forename='Technie', surname='Technicsen')
        expected = c.Client(name='SomeCo', contacts=[boss, techie])

        actual = to_model(
            {'entity': 'Client', 'name': 'SomeCo',
             'contacts': [{'entity': 'Contact', 'forename': 'Bossy',
                           'surname': 'McBoss'},
                          {'entity': 'Contact', 'forename': 'Technie',
                           'surname': 'Technicsen'}]}, c)

        self.assertModelsEqual(expected, actual)
