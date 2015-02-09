from collections import OrderedDict

from flask import request, jsonify

from planner.model.connect import transaction


class EntityTranslationError(Exception):
    pass


def crudify(app, read=None, delete=None, update=None, create=None):
    if read:
        read.register(Read, app)
    if delete:
        delete.register(Delete, app)
    if create:
        create.register(Create, app)


class Api(object):
    __apientityname__ = None
    __apifields__ = None

    def to_dict(self):
        d = OrderedDict()
        d['entity'] = self.__apientityname__
        for field in self.__apifields__:
            try:
                d[field] = self.__getattribute__(field)
                if not isinstance(d[field], OrderedDict):
                    d[field] = d[field].to_dict()
            except Exception:
                d[field] = None

        return d

    @staticmethod
    def from_dict(cls, data):
        if data['entity'] != cls.__apientityname__:
            raise EntityTranslationError

        try:
            r = cls()
            for field in cls.__apifields__:
                r.__setattr__(field, data[field])
        except KeyError:
            raise EntityTranslationError

        return r

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()


class Routes(object):
    def __init__(self, prefix, *models):
        self.prefix = prefix
        self.models = models

    def register(self, method, app):
        for model in self.models:
            app.add_url_rule(self.url(model), self.name(model), method(model),
                             methods=['POST'])

    def url(self, model):
        return self.prefix + model.__apientityname__

    def name(self, model):
        return self.prefix.replace('/', '_')[1:] + model.__apientityname__


class Read(object):
    def __init__(self, model):
        self.model = model

    def __call__(self):
        with transaction() as db:
            return jsonify(data=map(db.query(self.model).all(),
                           lambda r: r.to_dict()))


class Create(object):
    def __init__(self, model):
        self.model = model

    def __call__(self):
        with transaction() as db:
            db.add(self.model.from_dict(request.get_json()))

        return "OK"


class Delete(object):
    def __init__(self, model):
        self.model = model

    def __call__(self):
        with transaction() as db:
            db.delete(db.query(self.model).filter_by(
                id=request.get_json()['id']).first()
            )

        return "OK"
