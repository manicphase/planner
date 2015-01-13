from __future__ import division


def cost(team, iterations):
    r = {}
    for iteration in iterations:
        r[iteration.startdate] = team.cost
    return r


def utilization(team, iterations, engagements):
    r = {}
    for iteration in iterations:
        r[iteration.startdate] = sum([engagement.probable_complexity for engagement in engagements if iteration in engagement.iterations]) / team.capacity
    return r


def revenue(team, iterations, engagements):
    r = {}
    for iteration in iterations:
        r[iteration.startdate] = sum([engagement.revenue for engagement in engagements if iteration in engagement.iterations])
    return r

