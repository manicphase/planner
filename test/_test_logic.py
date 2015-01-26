import unittest

from planner.logic import revenue
from test.stubs import StubIteration, StubEngagement


class TestLogic(unittest.TestCase):
    def test_revenue_one_actual_iteration_should_be_engagement_revenue(self):
        engagement = StubEngagement(revenue=100, actual=[StubIteration()])
        expected = engagement.revenue

        actual = revenue(engagement)

        self.assertEquals(expected, actual)
