from collections import OrderedDict
import pdb

from flask import request, jsonify


class EntityTranslationError(Exception):
    pass


def crudify(app, read=None, delete=None, update=None, create=None):
    if read:
        read.register(Read, app, methods=['GET'])
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
                d[field] = getattr(self, field)
                if not isinstance(d[field], OrderedDict):
                    d[field] = d[field].to_dict()
            except Exception:
                d[field] = None

        return d

    @classmethod
    def from_dict(cls, data):
        try:
            if data.get('entity') != cls.__apientityname__:
                raise EntityTranslationError

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

    def register(self, method, app, methods=['POST']):
        for model in self.models:
            app.add_url_rule(self.url(model), self.name(model),
                             method(app.transaction, model),
                             methods=methods)

    def url(self, model):
        return self.prefix + model.__apientityname__

    def name(self, model):
        return self.prefix.replace('/', '_')[1:] + model.__apientityname__


class Read(object):
    def __init__(self, transaction, model):
        self.model = model
        self.transaction = transaction

    def __call__(self):
        with self.transaction() as db:
            return jsonify(data=map(lambda r: r.to_dict(),
                                    db.query(self.model).all()))


class Create(object):
    def __init__(self, transaction, model):
        self.model = model
        self.transaction = transaction

    def __call__(self):
        with self.transaction() as db:
            pdb.set_trace()
            data = request.get_json()
            db.add(self.model.from_dict(data))

        return "OK"


class Delete(object):
    def __init__(self, transaction, model):
        self.model = model
        self.transaction = transaction

    def __call__(self):
        with self.transaction() as db:
            db.delete(db.query(self.model).filter_by(
                id=request.get_json()['id']).first()
            )

        return "OK"
