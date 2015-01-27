from __future__ import division

from planner.config import RND_TAX_CREDIT


__all__ = ['revenue', 'finance', 'utilization']


def certain_rnd_revenue(e):
    return e.team.cost * RND_TAX_CREDIT if e.isrnd else 0.0


def certain_iteration_revenue(e):
    return e.revenue + certain_rnd_revenue(e)


def probable_iteration_revenue(e):
    return certain_iteration_revenue(e) * e.probability


def certain_iterations(e):
    return len(e.actual)


def probable_iterations(e):
    return len(e.estimated)


def certain_engagement_revenue(e):
    return certain_iteration_revenue(e) * certain_iterations(e)


def probable_engagement_revenue(e):
    return probable_iteration_revenue(e) * probable_iterations(e)


def revenue(e):
    return certain_engagement_revenue(e) + probable_iteration_revenue(e)


def finance(team, iterations, engagements):
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
                 'data': [sum([engagement.revenue *
                               float(engagement.probability)
                               for engagement in engagements
                               if iteration in engagement.actual
                               or iteration in engagement.estimated])
                          for iteration in iterations]}]}


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
