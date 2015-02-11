from sqlalchemy.exc import IntegrityError

from test import ModelTestCase
from planner.model.iteration import Iteration


class TestIteration(ModelTestCase):
    def test_iteration_should_have_a_start_date(self):
        with self.assertRaises(IntegrityError):
            with self.transaction() as db:
                db.add(Iteration(startdate=None))
