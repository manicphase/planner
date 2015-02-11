from flask import Flask, abort, current_app, render_template, Blueprint

from planner.model.connect import TransactionFactory
from planner.flags import Flag
from planner.config import HeadConfig


ui = Blueprint('views', __name__, template_folder="templates")
api = Blueprint('api', __name__, template_folder="templates")
feature = Flag(lambda: abort(404), config=lambda: current_app.config)


def create_app(config=HeadConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(ui)
    app.register_blueprint(api)
    app.transaction = TransactionFactory(
        app.config['DBPATH'], create_all=app.config.get("DBCREATE"))

    return app


@ui.route('/')
@feature
def index():
    return "TODO: fix the templates"


@ui.route('/schedule')
@feature
def schedule():
    return render_template('schedule.html')


@ui.route('/add-engagement')
@feature
def add_engagement():
    return render_template('add-engagement.html')


@ui.route('/clients')
@feature
def clients():
    return render_template("clients.html")


@ui.route('/add-client')
@feature
def add_client():
    return render_template("add-client.html")


@ui.route('/add-contact')
@feature
def add_contact():
    return render_template('add-contact.html')


@api.route('/api/schedule/iteration-for-engagement')
@feature
def schedule_iteration_for_engagement(self):
    pass
