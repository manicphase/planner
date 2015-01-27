from __future__ import division


def revenue(engagement):
    rndrev = engagement.team.cost * 0.25 if engagement.isrnd else 0
    prndrev = rndrev * engagement.probability
    rev = engagement.revenue
    prev = rev * engagement.probability
    return sum([prev * len(engagement.estimated),
                rev * len(engagement.actual),
                rndrev * len(engagement.actual),
                prndrev * len(engagement.estimated)])


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
