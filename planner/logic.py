def prioritize(engagement, team, s_weight=1.0, a_weight=0.5, r_weight=0.8):
    wsum = s_weight + a_weight + r_weight
    s = weight(engagement.sustainability, s_weight, wsum)
    a = weight(engagement.alignment, a_weight, wsum)
    r = weight(engagement.revenue / team.revenue_cap, r_weight, wsum)

    return s + a + r, engagement


def weight(raw, weighting, weighting_sum):
    assert raw >= 0 and factor.raw <= 1
    assert weighting <= weighting_sum

    return (raw * weighting) * (weighting / weighting_sum)


def tax_credit_value(team, engagement, tax_credit_value=0.25):
    # TODO: overall tax credit value cannot be more than .25 of wages
    assert team.cost >= 0
    assert engagement.complexity >= 0
    assert team.capacity >= 0

    return ((team.capacity * engagement.complexity) * team.cost) * tax_credit_value)


def probable_engagement_revenue(engagement):
    assert engagement.revenue >= 0
    assert engagement.probability <= 1.0 and engagement.probability >= 0
    
    return actual_engagement_revenue(engagement) + (len(engagement.estimatediter) * engagement.probability) * engagement.revenue)


def actual_engagement_revenue(engagement):
    assert engagement.revenue >= 0
    
    return len(engagement.actualiter) * engagement.revenue

