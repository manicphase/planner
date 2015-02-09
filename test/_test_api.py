import unittest

from planner.api import Api, EntityTranslationError


class Dummy(Api):
    __apientityname__ = 'Dummy'
    __apifields__ = ['one', 'two']

    def __init__(self, one='alpha', two='beta'):
        self.one = one
        self.two = two


class TestApi(unittest.TestCase):
    def test_to_dict_without_all_keys_should_fail(self):
        with self.assertRaises(EntityTranslationError):
            Dummy.from_dict({'entity': 'Dummy'})

    def test_to_dict_with_wrong_entity_should_fail(self):
        with self.assertRaises(EntityTranslationError):
            Dummy.from_dict({'entity': 'Wrong'})

    def test_api_should_be_equal_when_fields_and_entity_match(self):
        left = Dummy()
        right = Dummy()

        self.assertEquals(left, right)
