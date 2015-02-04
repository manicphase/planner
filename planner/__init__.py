from flask import (
    Flask, render_template, redirect, url_for, request, flash, jsonify
)

from planner.logic import utilization, finance
from planner.form import NewEngagement, NewContact
from planner.model import (
    Team, Iteration, Engagement, ActualEngagementIteration,
    EstimatedEngagementIteration, Contact
)
from planner.model.connect import LiveSession
from config import SECRET_KEY


app = Flask(__name__)
app.db = LiveSession
app.secret_key = SECRET_KEY


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/schedule')
def schedule():
    session = app.db()
    iterations = session.query(Iteration).all()
    engagements = session.query(Engagement).all()

    return render_template('schedule.html',
                           iterations=iterations, engagements=engagements)


@app.route('/add-engagement', methods=['POST', 'GET'])
def add_engagement():
    session = app.db()
    if request.method == 'POST':
        form = NewEngagement(request.form)
        if form.validate():
            session.add(Engagement(teamid=1,
                                   name=form.name.data,
                                   client=form.client.data,
                                   sowlink=form.sowlink.data,
                                   probability=form.probability.data,
                                   sustainability=form.sustainability.data,
                                   alignment=form.alignment.data,
                                   revenue=form.revenue.data,
                                   status=form.status.data,
                                   complexity=form.complexity.data,
                                   isrnd=form.isrnd.data))
            session.commit()
            flash("Added engagement")
            session.close()

            return redirect(url_for('index'))
        else:
            flash("Invalid submission")
            session.close()

            return render_template('add-engagement.html', form=form)
    session.close()

    return render_template('add-engagement.html', form=NewEngagement())


@app.route('/api/schedule/iteration-for-engagement', methods=['POST'])
def api_schedule_iteration_for_engagement():
    data = request.get_json()
    message = "FAIL"
    session = app.db()
    engagement = session.query(Engagement).filter_by(
        id=data['engagement']).first()
    if data['status'] == 'removed':
        session.execute(ActualEngagementIteration.delete().where(
            'iterationid=%s and engagementid=%s' % (data['iteration'],
                                                    data['engagement'])))
        session.execute(EstimatedEngagementIteration.delete().where(
            'iterationid=%s and engagementid=%s' % (data['iteration'],
                                                    data['engagement'])))
        message = jsonify(id="iter%s_eng%s" % (
            data['iteration'], data['engagement']), value=0, status='removed')
    elif data['status'] == 'actual':
        session.execute(EstimatedEngagementIteration.delete().where(
            'iterationid=%s and engagementid=%s' % (data['iteration'],
                                                    data['engagement'])))
        session.execute(ActualEngagementIteration.insert().values(
            engagementid=data['engagement'], iterationid=data['iteration']))
        message = jsonify(id="iter%s_eng%s" % (
            data['iteration'], data['engagement']),
            value=engagement.complexity, status='actual')
    elif data['status'] == 'estimated':
        session.execute(ActualEngagementIteration.delete().where(
            'iterationid=%s and engagementid=%s' % (data['iteration'],
                                                    data['engagement'])))
        session.execute(EstimatedEngagementIteration.insert().values(
            engagementid=data['engagement'], iterationid=data['iteration']))
        message = jsonify(id="iter%s_eng%s" % (
            data['iteration'], data['engagement']),
            value=engagement.probable_complexity(), status='estimated')
    session.commit()
    session.close()

    return message


@app.route('/api/data', methods=['POST'])
def api_data():
    data = request.get_json()
    message = "FAIL"
    session = app.db()
    team = session.query(Team).filter_by(id=data['team']).first()
    iterations = session.query(Iteration).all()  # TODO: filter by date range
    engagements = team.engagements
    if data['set'] == 'finance':
        message = jsonify(finance(team, iterations, engagements))
    elif data['set'] == 'utilization':
        message = jsonify(utilization(team, iterations, engagements))

    return message


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
