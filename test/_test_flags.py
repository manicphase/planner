import unittest

from planner.flags import Flag


class TestFlags(unittest.TestCase):
    def test_feature_enabled_should_call_func(self):
        func = lambda: True
        func.__name__ = "FunctionA"
        default_func = lambda: False
        flag_wrapper = Flag(default_func)

        wrapped = flag_wrapper(func)

        self.assertTrue(wrapped())

    @unittest.skip("Not yet implemented flag configs")
    def test_feature_disabled_should_call_default_func(self):
        func = lambda: True
        func.__name__ = "DisabledFunctionA"
        default_func = lambda: False
        flag_wrapper = Flag(default_func)

        wrapped = flag_wrapper(func)

        self.assertFalse(wrapped())
