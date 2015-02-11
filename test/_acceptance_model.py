import datetime

from test import ModelTestCase
from planner.model.iteration import Iteration, EstimatedIteration
from planner.model.engagement import (
    Engagement, Status, Complexity, Probability, Alignment, Sustainability,
    Expense, ExpenseType
)
from planner.model.team import Team, Cost, CostType, TeamMember
from planner.model.client import Client, Contact


class ModelAcceptanceTests(ModelTestCase):
    def test_can_add_team_with_iterations_with_engagements_with_clients(self):
        tm_one = TeamMember(
            forename="One", surname="Test", title="Mr",
            gmail="one.test@example.com", mobileno="0712345678",
            twitter="@onetest", github="http://github.com/onetest",
            picture="onetest.png", bio="Just a testy tester")
        tm_two = TeamMember(
            forename="Two", surname="Test", title="Dr",
            gmail="two.test@gmail.com", mobileno="07123456789",
            twitter="@drtwotests", github="http://github.com/drtwotests",
            picture="twotest.png", bio="Evil Dr Two Tests")

        wages = CostType(name="Wages")
        training = CostType(name="Training")
        tm_one_wages = Cost(value=5, teammember=tm_one, type=wages)
        tm_one_training = Cost(value=100, teammember=tm_one, type=training)
        tm_two_wages = Cost(value=50, teammember=tm_two, type=wages)

        team = Team(name="Test", capacity=1.0, revenuecap=100, devmax=0.2,
                    researchmax=0.1, members=[tm_one, tm_two])

        travel = ExpenseType(name="Travel")
        systems = ExpenseType(name="Systems")
        unpaid_travel_expense = Expense(value=5, trackerid="0001", paid=False,
                                        type=travel)
        paid_travel_expense = Expense(value=5, trackerid="0002", paid=True,
                                      type=travel)
        unpaid_systems_expense = Expense(value=100, trackerid="0003",
                                         paid=False, type=systems)

        bankmgr = Contact(forename="Bank", surname="Manager")
        banktechie = Contact(forename="Bank", surname="Techie")
        agencymgr = Contact(forename="Agency", surname="Manager")
        bank = Client(name="Bank", contacts=[bankmgr, banktechie])
        agency = Client(name="Agency", contacts=[agencymgr])
        sold = Status(name="Sold")
        negotiation = Status(name="Negotiation")
        small = Complexity(name="Small", value=0.5)
        p_certain = Probability(name="Certain", value=1.0)
        a_evens = Alignment(name="Evens", value=0.5)
        s_evens = Sustainability(name="Evens", value=0.5)
        p_evens = Probability(name="Evens", value=0.5)

        sold_engagement = Engagement(
            name="SoldEngagement", revenue=1000, proposal="SomeProposal",
            backlog="SomeBacklog", isrnd=False, ponumber="999", team=team,
            client=bank, status=sold, complexity=small, probability=p_certain,
            sustainability=s_evens, alignment=a_evens,
            expenses=[unpaid_travel_expense, paid_travel_expense,
                      unpaid_systems_expense])
        negotiation_engagement = Engagement(
            name="NegotiationEngagement", revnue=1000, team=team,
            client=agency, status=negotiation, complexity=small,
            probability=p_evens, sustainability=s_evens, alignment=a_evens,
            expenses=[])

        a_it_one = Iteration(startdate=datetime.date(2015, 01, 01),
                             engagements=[sold_engagement])
        e_it_one = EstimatedIteration(
            startdate=datetime.date(2015, 01, 01),
            engagements=[negotiation_engagement])

        with self.transaction() as db:
            db.add(tm_one_training)
            db.add(tm_one_wages)
            db.add(tm_two_wages)
            db.add(a_it_one)
            db.add(e_it_one)
