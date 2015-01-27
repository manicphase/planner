class StubIteration(object):

    def __init__(self):
        pass


class StubTeam(object):

    def __init__(self, cost=0):
        self.cost = cost


class StubEngagement(object):
    def __init__(self, isrnd=False, revenue=0, probability=0.0, actual=[],
                 estimated=[], team=StubTeam()):
        self.revenue = revenue
        self.actual = actual
        self.probability = probability
        self.estimated = estimated
        self.isrnd = isrnd
        self.team = team
