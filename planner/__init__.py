from flask import Flask, render_template, redirect, url_for, request, flash

from planner.model import LiveSession, Engagement
from planner.form import NewEngagement, ModifyEngagement 
from config import SECRET_KEY


app = Flask(__name__)
app.db = LiveSession
app.secret_key = SECRET_KEY


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin')
def admin():
    session = app.db()
    engagements = session.query(Engagement).all()
    session.close()
    return render_template('admin.html', engagements=engagements)


@app.route('/admin/add-engagement', methods=['POST', 'GET'])
def add_engagement():
    if request.method == 'POST':
        form = NewEngagement(request.form)
        if form.validate():
            session = app.db()
            try:
                session.add(Engagement(teamid=form.team.data,
                                       client=form.client.data,
                                       project=form.project.data,
                                       sowlink=form.sowlink.data,
                                       probability=form.probability.data,
                                       sustainability=form.sustainability.data,
                                       alignment=form.alignment.data,
                                       revenue=form.revenue.data,
                                       status=form.status.data,
                                       complexity=form.complexity.data,
                                       type=form.type.data))

                session.commit()
                flash("Successfully added engagement!")
                return redirect(url_for('admin'))
            except:
                flash("Something went wrong")
            finally:
                session.close()
        else:
            flash("Form submission failed")
    else:
        form = NewEngagement()
    return render_template('add-engagement.html', form=form)


@app.route('/admin/modify-engagement/<engagementid>', methods=['POST', 'GET'])
def modify_engagement(engagementid):
    if request.method == 'POST':
        form = ModifyEngagement(request.form)
        if form.validate():
            session = app.db()
            try:
                engagement = session.query(Engagement).filter_by(id=engagementid).first()
                if form.team.data:
                    engagement.teamid = form.team.data
                if form.client.data:
                    engagement.client = form.client.data
                if form.project.data:
                    engagement.project = form.project.data
                if form.sowlink.data:
                    engagement.sowlink = form.sowlink.data
                if form.probability.data:
                    engagement.probability = form.probability.data
                if form.sustainability.data:
                    engagement.sustainability = form.sustainability.data
                if form.alignment.data:
                    engagement.alignment = form.alignment.data
                if form.revenue.data:
                    engagement.revenue = form.revenue.data
                if form.type.data:
                    engagement.type = form.type.data
                session.add(engagement)
                session.commit()
                flash("Successfully added engagement!")
                return redirect(url_for('admin'))
            except:
                flash("Something went wrong")
            finally:
                session.close()
        else:
            flash("Form submission failed")
    else:
        form = ModifyEngagement()
        form.engagementid = engagementid
    return render_template('modify-engagement.html', form=form)

