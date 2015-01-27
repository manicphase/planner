import unittest

from planner.logic import revenue
from test.stubs import StubIteration, StubEngagement, StubTeam


class TestLogic(unittest.TestCase):
    def test_one_actual_should_be_engagement_revenue(self):
        engagement = StubEngagement(revenue=100, actual=[StubIteration()])
        expected = engagement.revenue

        actual = revenue(engagement)

        self.assertEquals(expected, actual)

    def test_one_estimated_should_be_function_of_probability_and_revenue(self):
        engagement = StubEngagement(revenue=100, probability=0.5,
                                    estimated=[StubIteration()])
        expected = engagement.revenue * engagement.probability

        actual = revenue(engagement)

        self.assertEquals(expected, actual)

    def test_rnd_should_be_a_factor_in_revenue(self):
        team = StubTeam(cost=100)
        engagement = StubEngagement(isrnd=True, actual=[StubIteration()],
                                    team=team)
        expected = team.cost * 0.25

        actual = revenue(engagement)

        self.assertEquals(expected, actual)
