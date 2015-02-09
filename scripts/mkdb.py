#!/usr/bin/env python

from datetime import date
from os.path import exists

from planner.config import LiveConfig
from planner.model import (
    Iteration, Team, EngagementComplexity, EngagementProbability,
    EngagementSustainability, EngagementAlignment, EngagementStatus
  )
from planner.model.connect import transaction


def static_live_data():
    with transaction() as session:
        for status in ['Lost', 'Approach', 'Negotiation', 'Sold', 'Complete']:
            session.add(EngagementStatus(name=status))
        for value, name in [(0.0, 'Certainly Unaligned'),
                            (0.1, 'Almost Certainly Unaligned'),
                            (0.2, 'Largely Unaligned'),
                            (0.3, 'Probably Unaligned'),
                            (0.4, 'Generally Unaligned'),
                            (0.5, 'Unsure'),
                            (0.6, 'Generally Aligned'),
                            (0.7, 'Probably Aligned'),
                            (0.8, 'Largely Aligned'),
                            (0.9, 'Almost Certainly Aligned'),
                            (1.0, 'Certainly Aligned')]:
            session.add(EngagementAlignment(value=value, name=name))
        for value, name in [(0.0, 'Impossible to Sustain'),
                            (0.1, 'Almost Impossible to Sustain'),
                            (0.2, 'Very Challenging to Sustain'),
                            (0.3, 'Challenging to Sustain'),
                            (0.4, 'Generally Unsustainable'),
                            (0.5, 'Unsure'),
                            (0.6, 'Generally Sustainable'),
                            (0.7, 'Easy to Sustain'),
                            (0.8, 'Very Easy to Sustain'),
                            (0.9, 'Almost Certain to Sustain'),
                            (1.0, 'Certain to Sustain')]:
            session.add(EngagementSustainability(name=name, value=value))
        for value, name in [(0.0, 'Lost'),
                            (0.1, 'Almost Lost'),
                            (0.2, 'Very Probably Lost'),
                            (0.3, 'Probably Lost'),
                            (0.4, 'Possibly Lost'),
                            (0.5, 'Unsure'),
                            (0.6, 'Possibly Won'),
                            (0.7, 'Probably Won'),
                            (0.8, 'Very Probably Won'),
                            (0.9, 'Almost Certainly Won'),
                            (1.0, 'Won')]:
            session.add(EngagementProbability(name=name, value=value))
        for value, name in [(0.1, 'Tiny'),
                            (0.5, 'Small'),
                            (1.0, 'Medium'),
                            (2.0, 'Large')]:
            session.add(EngagementComplexity(name=name, value=value))
        for d in [date(2015, 1, 5), date(2015, 1, 19), date(2015, 2, 2),
                  date(2015, 2, 16), date(2015, 3, 2), date(2015, 3, 16),
                  date(2015, 3, 30), date(2015, 4, 13), date(2015, 4, 27),
                  date(2015, 5, 11), date(2015, 5, 25), date(2015, 6, 8),
                  date(2015, 6, 22), date(2015, 7, 6), date(2015, 7, 20),
                  date(2015, 8, 3), date(2015, 8, 17), date(2015, 8, 31),
                  date(2015, 9, 14), date(2015, 9, 28), date(2015, 10, 12),
                  date(2015, 10, 26), date(2015, 11, 9), date(2015, 11, 23),
                  date(2015, 12, 7), date(2015, 12, 21)]:
            session.add(Iteration(startdate=d))


if __name__ == '__main__':
    engine = create_engine(LiveConfig.LIVEDBPATH)
    Base.metadata.create_all()
    static_live_data()
    print "DB created"
