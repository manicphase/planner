from test import ModelTestCase
from planner.model import ValidationError
from planner.model.team import Team, TeamMember, Cost, CostType


class TestTeam(ModelTestCase):
    def test_team_should_have_a_unique_name(self):
        self.assertHasUniqueName(Team, capacity=1.0, revenuecap=1, devmax=0.4,
                                 researchmax=0.6)


class TestTeamMember(ModelTestCase):
    def test_team_member_should_have_forename(self):
        self.assertHasAttribute(
            TeamMember, "forename", surname="", title="Mr", gmail="@",
            twitter="", github="", picture="", bio="", mobileno="0712345678")

    def test_team_member_should_have_surname(self):
        self.assertHasAttribute(
            TeamMember, "surname", forename="", title="Mr", gmail="@",
            twitter="", github="", picture="", bio="", mobileno="0712345678")

    def test_team_member_should_have_appropriate_title(self):
        member = TeamMember(forename="", surname="", gmail="@", twitter="",
                            github="", picture="", bio="",
                            mobileno="0712345678")
        for bad_title in ['007', '', '*', 'Supreme Commander North Atlantic Treaty Organization Forces, European Union']:  # noqa
            with self.assertRaises(ValidationError):
                with self.transaction() as db:
                    member.title = bad_title
                    db.add(member)

        for good_title in ['Mr', 'Dr', 'Miss', 'Mrs']:
            try:
                with self.transaction() as db:
                    member.title = good_title
                    db.add(member)
            except:
                raise AssertionError(good_title + " should be valid but isnt")

    def test_team_member_should_have_appropriate_gmail(self):
        member = TeamMember(forename="", surname="", gmail="@", twitter="",
                            github="", picture="", bio="", title="Mr",
                            mobileno="0712345678")

        with self.transaction(rollback=True) as db:
            db.add(member)

        with self.assertRaises(ValidationError):
            with self.transaction() as db:
                member.gmail = "notvalid.com"
                db.add(member)

    def test_team_member_should_have_twitter(self):
        self.assertHasAttribute(
            TeamMember, "twitter", forename="", title="Mr", gmail="@",
            surname="", github="", picture="", bio="", mobileno="0712345678")

    def test_team_member_should_have_github(self):
        self.assertHasAttribute(
            TeamMember, "github", forename="", title="Mr", gmail="@",
            surname="", twitter="", picture="", bio="", mobileno="0712345678")

    def test_team_member_should_have_picture(self):
        self.assertHasAttribute(
            TeamMember, "picture", forename="", title="Mr", gmail="@",
            surname="", twitter="", github="", bio="", mobileno="0712345678")

    def test_team_member_should_have_bio(self):
        self.assertHasAttribute(
            TeamMember, "picture", forename="", title="Mr", gmail="@",
            surname="", twitter="", github="", bio="", mobileno="0712345678")

    def test_team_member_mobileno_should_be_valid_uk_mobileno(self):
        self.assertHasValidUkMobileNumber(
            TeamMember, forename="", title="Mr", gmail="@", surname="",
            twitter="", github="", bio="", picture="")


class TestCost(ModelTestCase):
    def test_cost_should_have_appropriate_value(self):
        self.assertHasValidAttribute(Cost, 'value', 0, low=0, unit=1)


class TestCostType(ModelTestCase):
    def test_cost_type_name_should_be_unique(self):
        self.assertHasUniqueName(CostType)
