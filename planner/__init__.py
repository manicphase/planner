from flask import Flask, render_template

from planner.model import (
    Iteration, Engagement, Client, ActualEngagementIteration,
    EstimatedEngagementIteration
)
from planner.util import Routes, crudify


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/schedule')
def schedule():
    return render_template('schedule')


@app.route('/add-engagement')
def add_engagement():
    return render_template('add-engagement.html')


crudify(app,
        read=Routes('/api/read/', Iteration, Engagement),
        delete=Routes('/api/delete/', ActualEngagementIteration,
                      EstimatedEngagementIteration, Engagement),
        create=Routes('/api/create/', Engagement, Client))
