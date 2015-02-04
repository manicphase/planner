from __future__ import division

from planner.config import RND_TAX_CREDIT


__all__ = ['engagement_revenue', 'iteration_revenue', 'iteration_complexity',
           'finance', 'utilization']


def _eirev(e):
    return e.revenue + (e.team.cost * RND_TAX_CREDIT if e.isrnd else 0.0)


def engagement_revenue(e):
    return (_eirev(e) * len(e.actual) +
            _eirev(e) * e.probability * len(e.estimated))


def iteration_revenue(i):
    return (sum(map(i.actual, _eirev)) +
            sum(map(i.estimated, lambda e: _eirev(e) * e.probability)))


def iteration_complexity(i):
    return (sum(map(i.actual, lambda e: e.complexity)) +
            sum(map(i.estimated, lambda e: e.complexity * e.probability)))


def finance(team, iterations):
    return {'labels': [str(i.startdate) for i in iterations],
            'datasets': [
                {'label': "Cost in GBP",
                 'fillColor': "rgba(255, 0, 0, 0.2)",
                 'strokeColor': "rgba(255, 0, 0, 1)",
                 'pointColor': "rgba(255, 0, 0, 1)",
                 'pointStrokeColor': "#fff",
                 'pointHighlightFill': "#fff",
                 'pointHighlightStroke': "rgba(255, 0, 0, 1)",
                 'data': [team.cost for i in iterations]},
                {'label': "Revenue in GBP",
                 'fillColor': "rgba(0, 255, 0, 0.2)",
                 'strokeColor': "rgba(0, 255, 0, 1)",
                 'pointColor': "rgba(0, 255, 0, 1)",
                 'pointStrokeColor': "#fff",
                 'pointHighlightFill': "#fff",
                 'pointHighlightStroke': "rgba(0, 255, 0, 1)",
                 'data': [iteration_revenue(i) for i in iterations]}]}


def utilization(team, iterations, engagements):
    return {'labels': [str(i.startdate) for i in iterations],
            'datasets': [
                {'label': u"Utilization in Percentage of Capacity",
                 'fillColor': "rgba(220, 220, 220, 0.2)",
                 'strokeColor': "rgba(220, 220, 220, 1)",
                 'pointColor': "rgba(220, 220, 220, 1)",
                 'pointStrokeColor': "#fff",
                 'pointHighlightFill': "#fff",
                 'pointHighlightStroke': "rgba(220, 220, 220, 1)",
                 'data': [iteration_complexity(i) for i in iterations]}]}
