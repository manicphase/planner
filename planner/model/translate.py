import datetime

from sqlalchemy.inspection import inspect


def to_dict(model):
    d = {'entity': model.__tablename__}
    for column in model.__table__.columns:
        d[column.name] = getattr(model, column.name)
    for relation in inspect(model.__class__).relationships:
        try:
            d[relation.key] = to_dict(getattr(model, relation.key))
        except AttributeError:
            d[relation.key] = map(to_dict, getattr(model, relation.key))

    return d


def to_model(data, module):
    model = getattr(module, data['entity'])()
    for key, value in data.iteritems():
        if key == 'entity':
            continue
        elif type(value) in [bool, str, unicode, int, float, datetime.date]:
            setattr(model, key, value)
        else:
            try:
                value.get('entity')
                setattr(model, key, to_model(value, module))
            except AttributeError:
                setattr(model, key, map(lambda m: to_model(m, module), value))

    return model
