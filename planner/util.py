from flask import request, jsonify

from planner.model.connect import transaction


class Routes(object):
    def __init__(self, prefix, *models):
        self.prefix = prefix
        self.models = models

    def register(self, method, app):
        for model in self.models:
            app.add_url_rule(self.url(model), self.name(model), method(model),
                             methods=['POST'])

    def url(self, model):
        return self.prefix + model.__tablename__

    def name(self, model):
        return self.prefix.replace('/', '_')[1:] + model.__tablename__


def crudify(app, read=None, delete=None, update=None, create=None):
    if read:
        read.register(Read, app)
    if delete:
        delete.register(Delete, app)
    if create:
        create.register(Create, app)


class Read(object):
    def __init__(self, model):
        self.model = model

    def __call__(self):
        with transaction() as db:
            jsonify(data=map(db.query(self.model).all(),
                             lambda r: r.to_dict()))


class Create(object):
    def __init__(self, model):
        self.model = model

    def __call__(self):
        with transaction() as db:
            db.add(self.model.from_dict(request.get_json()))


class Delete(object):
    def __init__(self, model):
        self.model = model

    def __call__(self):
        with transaction() as db:
            db.delete(db.query(self.model).filter_by(
                id=request.get_json()['id']).first()
            )
