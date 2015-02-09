from flask import Flask, render_template

from planner.model import (
    Iteration, Engagement, Contact, Client
)
from planner.api import Routes, crudify


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/schedule')
def schedule():
    return render_template('schedule.html')


@app.route('/add-engagement')
def add_engagement():
    return render_template('add-engagement.html')


@app.route('/clients')
def clients():
    return render_template("clients.html")


@app.route('/add-client')
def add_client():
    return render_template("add-client.html")


@app.route('/add-contact')
def add_contact():
    return render_template('add-contact.html')


@app.route('/api/schedule/iteration-for-engagement')
def schedule_iteration_for_engagement(self):
    pass


crudify(app,
        read=Routes('/api/read/', Iteration),
        create=Routes('/api/create/', Engagement, Client, Contact))
