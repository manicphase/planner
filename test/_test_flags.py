import unittest

from planner import create_app
from planner.flags import Flag
from planner.config import HeadConfig, StableConfig


class TestFlags(unittest.TestCase):
    def test_feature_enabled_should_call_func(self):
        func = lambda: True
        func.__name__ = "FunctionA"
        default_func = lambda: False
        flag_wrapper = Flag(default_func)

        wrapped = flag_wrapper(func)

        self.assertTrue(wrapped())

    def test_feature_disabled_should_call_default_func(self):
        func = lambda: True
        func.__name__ = "A"
        default_func = lambda: False
        flag_wrapper = Flag(default_func,
                            config=lambda: {"DISABLED_FEATURES": ["A"]})

        wrapped = flag_wrapper(func)

        self.assertFalse(wrapped())

    def test_page_should_be_hidden_when_feature_disabled(self):
        app = create_app(StableConfig)
        client = app.test_client()
        resp = client.get('/')
        self.assertEqual(resp.status_code, 404)

    def test_page_should_show_when_feature_is_enabled(self):
        app = create_app(HeadConfig)
        client = app.test_client()
        resp = client.get('/')
        self.assertEqual(resp.status_code, 200)
