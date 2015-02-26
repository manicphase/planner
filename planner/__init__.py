from flask import (Flask, abort, current_app, render_template,
                   Blueprint, send_from_directory)

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
    return render_template('index.html')


@ui.route('/static/<path:filename>')
@feature
def serve_static_files(filename):
    import glob
    print glob.glob("planner/*")
    return send_from_directory("static/", filename)


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


@api.route('/api/schedule/engagement_iterations')
@feature
def engagement_iterations():
    # access db and that
    demo_json = '{"cost":[[1420416000000.0,500],[1421625600000.0,500],' + \
                '[1422835200000.0,500],[1424044800000.0,500]],' + \
                '"revenue":[[1420416000000.0,0],[1421625600000.0,100],' + \
                '[1422835200000.0,500],[1424044800000.0,2000]]}'
    return demo_json
    pass


@api.route('/api/schedule/engagement_iterations/<iteration>')
@feature
def single_engagement_iteration(iteration):
    # access db and that
    return iteration
    pass
