from test import ModelTestCase
from planner.model.engagement import (
    Status, Alignment, Sustainability, Probability, Complexity
)


class TestStatus(ModelTestCase):
    def test_engagement_status_should_always_have_a_unique_name(self):
        self.assertHasUniqueName(Status)


class TestAlignment(ModelTestCase):
    def test_engagement_alignment_should_always_have_a_unique_name(self):
        self.assertHasUniqueName(Alignment, value=1.0)

    def test_engagement_alignment_should_always_have_a_valid_value(self):
        self.assertHasValidAttribute(
            Alignment, 'value', 0.0, low=0.0, high=1.0, unit=0.1, unique=True,
            name="Name")


class TestSustainability(ModelTestCase):
    def test_engagement_sustainability_should_always_have_a_unique_name(self):
        self.assertHasUniqueName(Sustainability, value=1)

    def test_engagement_sustainability_should_always_have_a_valid_value(self):
        self.assertHasValidAttribute(
            Sustainability, 'value', 0.1, unique=True,
            low=0.0, high=1.0, unit=0.1, name="Name")


class TestProbability(ModelTestCase):
    def test_engagement_probability_should_always_have_a_unique_name(self):
        self.assertHasUniqueName(Probability, value=0.5)

    def test_engagement_probability_should_always_have_a_valid_value(self):
        self.assertHasValidAttribute(
            Probability, 'value', 0.1, unique=True, name="Name",
            low=0.0, high=1.0, unit=0.1)


class TestComplexity(ModelTestCase):
    def test_engagement_complexity_should_always_have_a_unique_name(self):
        self.assertHasUniqueName(Complexity, value=0.5)

    def test_engagement_complexity_should_always_have_a_valid_value(self):
        self.assertHasValidAttribute(
            Complexity, 'value', 0.1, unique=True,
            valid_set=[0.1, 0.5, 1.0, 2.0], invalid_set=[2.1, 0.0, 'one'],
            name="Name")
