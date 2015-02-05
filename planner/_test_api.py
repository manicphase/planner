import unittest
from collections import OrderedDict

from planner.model.api import Api, EntityTranslationError


class Dummy(Api):
    __apientityname__ = 'Dummy'
    __apifields__ = ['one', 'two']
    one = None
    two = None

    def __init__(self, one='alpha', two='beta'):
        self.one = one
        self.two = two


class TestApi(unittest.TestCase):
    def test_to_dict_works(self):
        expected = OrderedDict()
        expected['entity'] = 'Dummy'
        expected['one'] = 'alpha'
        expected['two'] = 'beta'

        self.assertEquals(expected, Dummy().to_dict())

    def test_from_dict_works(self):
        data = OrderedDict()
        data['entity'] = 'Dummy'
        data['one'] = 'beta'
        data['two'] = 'alpha'

        self.assertEquals(Dummy(one='beta', two='alpha'),
                          Dummy.from_dict(Dummy, data))

    def test_to_dict_without_all_keys_should_fail(self):
        with self.assertRaises(EntityTranslationError):
            Dummy.from_dict(Dummy, {'entity': 'Dummy'})

    def test_to_dict_with_wrong_entity_should_fail(self):
        with self.assertRaises(EntityTranslationError):
            Dummy.from_dict(Dummy, {'entity': 'Wrong'})
