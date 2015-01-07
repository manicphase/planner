def prioritize(engagement, s_weight=1.0, a_weight=0.5, r_weight=0.8):
    wsum = s_weight + a_weight + r_weight
    s = weight(engagement.sustainability, s_weight, wsum)
    a = weight(engagement.alignment, a_weight, wsum)
    r = weight(engagement.revenue / engagement.team.revenue_cap, r_weight, wsum)

    return s + a + r, engagement


def weight(raw, weighting, weighting_sum):
    assert raw >= 0 and factor.raw <= 1
    assert weighting <= weighting_sum

    return (raw * weighting) * (weighting / weighting_sum)

