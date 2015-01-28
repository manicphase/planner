from __future__ import division

from planner.config import RND_TAX_CREDIT


__all__ = ['engagement_revenue', 'iteration_revenue', 'finance', 'utilization']


def certain_rnd_revenue(e):
    return e.team.cost * RND_TAX_CREDIT if e.isrnd else 0.0


def certain_iteration_engagement_revenue(e):
    return e.revenue + certain_rnd_revenue(e)


def probable_iteration_engagement_revenue(e):
    return certain_iteration_engagement_revenue(e) * e.probability


def certain_iterations(e):
    return len(e.actual)


def probable_iterations(e):
    return len(e.estimated)


def certain_engagement_revenue(e):
    return certain_iteration_engagement_revenue(e) * certain_iterations(e)


def probable_engagement_revenue(e):
    return probable_iteration_engagement_revenue(e) * probable_iterations(e)


def engagement_revenue(e):
    return certain_engagement_revenue(e) + probable_engagement_revenue(e)


def iteration_revenue(i):
    t = 0
    for e in i.actual:
        t += certain_iteration_engagement_revenue(e)
    for e in i.estimated:
        t += probable_iteration_engagement_revenue(e)
    return t


def finance(team, iterations):
    return {'labels': [str(iteration.startdate) for iteration in iterations],
            'datasets': [
                {'label': "Cost in GBP",
                 'fillColor': "rgba(255, 0, 0, 0.2)",
                 'strokeColor': "rgba(255, 0, 0, 1)",
                 'pointColor': "rgba(255, 0, 0, 1)",
                 'pointStrokeColor': "#fff",
                 'pointHighlightFill': "#fff",
                 'pointHighlightStroke': "rgba(255, 0, 0, 1)",
                 'data': [team.cost for iteration in iterations]},
                {'label': "Revenue in GBP",
                 'fillColor': "rgba(0, 255, 0, 0.2)",
                 'strokeColor': "rgba(0, 255, 0, 1)",
                 'pointColor': "rgba(0, 255, 0, 1)",
                 'pointStrokeColor': "#fff",
                 'pointHighlightFill': "#fff",
                 'pointHighlightStroke': "rgba(0, 255, 0, 1)",
                 'data': [iteration_revenue(i) for i in iterations]}]}


def utilization(team, iterations, engagements):
    return {'labels': [str(iteration.startdate) for iteration in iterations],
            'datasets': [
                {'label': u"Utilization in Percentage of Capacity",
                 'fillColor': "rgba(220, 220, 220, 0.2)",
                 'strokeColor': "rgba(220, 220, 220, 1)",
                 'pointColor': "rgba(220, 220, 220, 1)",
                 'pointStrokeColor': "#fff",
                 'pointHighlightFill': "#fff",
                 'pointHighlightStroke': "rgba(220, 220, 220, 1)",
                 'data': [sum([engagement.probable_complexity()
                               for engagement in engagements
                               if iteration in engagement.actual
                               or iteration in engagement.estimated])
                          / team.capacity for iteration in iterations]}]}
