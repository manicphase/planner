from flask import Flask, render_template, request, redirect, url_for, flash
from planner.form import NewContact
from planner.model import (
    Iteration, Engagement, ActualEngagementIteration,
    EstimatedEngagementIteration, Contact, Client
)
from planner.model.connect import LiveSession
from planner.util import Routes, crudify


app = Flask(__name__)

app.db = LiveSession


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
    # TODO: Swap link from to client when created, naming page 'clients.html'
    session = app.db()
    engagements = session.query(Engagement).all()
    return render_template("clients.html", clients=engagements)


@app.route('/clients/<client_id>')
def contact_sheet(client_id):
    session = app.db()
    c = session.query(Contact).join(Engagement).filter_by(id=client_id)
    return render_template("contacts.html", clients=c, client_id=client_id)


@app.route('/clients/<client_id>/new', methods=['POST', 'GET'])
def add_contact(client_id):  # TODO: Not expose client ids
    if request.method == "GET":
        return render_template(
            'add-contact.html',
            form=NewContact(),
            client_id=client_id
            )
    if request.method == "POST":
        session = app.db()
        form = NewContact(request.form)
        if form.validate():
            session.add(Contact(forename=form.forename.data,
                                surname=form.surname.data,
                                email=form.email.data,
                                landlinenumber=form.landline.data,
                                role=form.role.data,
                                address=form.address.data,
                                mobilenumber=form.mobile.data,
                                client=client_id
                                ))
            session.commit()
            flash("Added Contact")
            session.close()

            return redirect(url_for('clients'))
        else:
            flash("Invalid submission")
            session.close()

            return render_template(
                'add-contact.html',
                form=form,
                client_id=client_id
                )

crudify(app,
        read=Routes('/api/read/', Iteration, Engagement),
        delete=Routes('/api/delete/', ActualEngagementIteration,
                      EstimatedEngagementIteration, Engagement),
        create=Routes('/api/create/', Engagement, Client))
