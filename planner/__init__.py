from flask import Flask, render_template

from planner.model import (
    Iteration, Engagement, Contact, Client
)
from planner.api import Routes, crudify
from flags import view_flag


app = Flask(__name__)


@app.route('/')
@view_flag
def index():
    return render_template('index.html')


@app.route('/schedule')
@view_flag
def schedule():
    return render_template('schedule.html')


@app.route('/add-engagement')
@view_flag
def add_engagement():
    return render_template('add-engagement.html')


@app.route('/clients')
@view_flag
def clients():
    return render_template("clients.html")


@app.route('/add-client')
@view_flag
def add_client():
    return render_template("add-client.html")


@app.route('/add-contact')
@view_flag
def add_contact():
    return render_template('add-contact.html')


@app.route('/api/schedule/iteration-for-engagement')
@view_flag
def schedule_iteration_for_engagement(self):
    pass


crudify(app,
        read=Routes('/api/read/', Iteration),
        create=Routes('/api/create/', Engagement, Client, Contact))
