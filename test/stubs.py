class StubEngagement(object):

    def __init__(self, revenue=0, probability=0.0, actual=[], estimated=[]):
        self.revenue = revenue
        self.actual = actual
        self.probability = probability
        self.estimated = estimated


class StubIteration(object):

    def __init__(self):
        pass
