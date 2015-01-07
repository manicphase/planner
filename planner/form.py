from wtforms import Form, FloatField, StringField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional


class NewEngagement(Form):
    team = SelectField(
            u'* Team',
            choices=[(1, 'TORG')],
            coerce=int,
            validators=[DataRequired()])
    client = StringField(u'* Client', validators=[DataRequired()])
    project = StringField(u'* Project', validators=[DataRequired()])
    sowlink = StringField(u'* Statement of Works Link', validators=[DataRequired()])
    probability = SelectField(
            u'* Probability',
            choices=[(0.0, '0%'), (0.1, '10%'), (0.2, '20%'), (0.3, '30%'),
                     (0.4, '40%'), (0.5, '50%'), (0.6, '60%'), (0.7, '70%'),
                     (0.8, '80%'), (0.9, '90%'), (1.0, '100%')],
            coerce=float,
            validators=[DataRequired()])
    sustainability = SelectField(
            u'* Sustainability',
            choices=[(0.1, '10%'), (0.2, '20%'), (0.3, '30%'),
                     (0.4, '40%'), (0.5, '50%'), (0.6, '60%'), (0.7, '70%'),
                     (0.8, '80%'), (0.9, '90%'), (1.0, '100%')],
            coerce=float,
            validators=[DataRequired()])
    alignment = SelectField(
            u'* Alignment',
            choices=[(0.0, '0%'), (0.1, '10%'), (0.2, '20%'), (0.3, '30%'),
                     (0.4, '40%'), (0.5, '50%'), (0.6, '60%'), (0.7, '70%'),
                     (0.8, '80%'), (0.9, '90%'), (1.0, '100%')],
            coerce=float,
            validators=[DataRequired()])
    revenue = IntegerField(u'* Revenue Per Iteration', validators=[DataRequired()])
    status = SelectField(
            u'* Status',
            choices=[(u'Complete', u'Complete'), (u'Sold', u'Sold'), (u'Negotiation', u'Negotiation'), (u'Approach', u'Approach'), (u'Lost', u'Lost')],
            coerce=unicode,
            validators=[DataRequired()])
    complexity = SelectField(
            u'* Complexity',
            choices=[(0.1, u'Tiny'), (0.5, u'Small'), (1.0, u'Medium'), (2.0, u'Large')],
            coerce=float,
            validators=[DataRequired()])
    type = SelectField(
            u'* Type',
            choices=[(u'Client', u'Client'), (u'Enablement', u'Enablement'), (u'Development', u'Development'), (u'Research', u'Research')],
            coerce=unicode,
            validators=[DataRequired()])


class ModifyEngagement(Form):
    team = SelectField(
            u'* Team',
            choices=[(1, 'TORG')],
            coerce=int,
            validators=[Optional()])
    client = StringField(u'* Client', validators=[Optional()])
    project = StringField(u'* Project', validators=[Optional()])
    sowlink = StringField(u'* Statement of Works Link', validators=[Optional()])
    probability = SelectField(
            u'* Probability',
            choices=[(0.0, '0%'), (0.1, '10%'), (0.2, '20%'), (0.3, '30%'),
                     (0.4, '40%'), (0.5, '50%'), (0.6, '60%'), (0.7, '70%'),
                     (0.8, '80%'), (0.9, '90%'), (1.0, '100%')],
            coerce=float,
            validators=[Optional()])
    sustainability = SelectField(
            u'* Sustainability',
            choices=[(0.1, '10%'), (0.2, '20%'), (0.3, '30%'),
                     (0.4, '40%'), (0.5, '50%'), (0.6, '60%'), (0.7, '70%'),
                     (0.8, '80%'), (0.9, '90%'), (1.0, '100%')],
            coerce=float,
            validators=[Optional()])
    alignment = SelectField(
            u'* Alignment',
            choices=[(0.0, '0%'), (0.1, '10%'), (0.2, '20%'), (0.3, '30%'),
                     (0.4, '40%'), (0.5, '50%'), (0.6, '60%'), (0.7, '70%'),
                     (0.8, '80%'), (0.9, '90%'), (1.0, '100%')],
            coerce=float,
            validators=[Optional()])
    revenue = IntegerField(u'* Revenue Per Iteration', validators=[Optional()])
    status = SelectField(
            u'* Status',
            choices=[(u'Complete', u'Complete'), (u'Sold', u'Sold'), (u'Negotiation', u'Negotiation'), (u'Approach', u'Approach'), (u'Lost', u'Lost')],
            coerce=unicode,
            validators=[Optional()])
    complexity = SelectField(
            u'* Complexity',
            choices=[(0.1, u'Tiny'), (0.5, u'Small'), (1.0, u'Medium'), (2.0, u'Large')],
            coerce=float,
            validators=[Optional()])
    type = SelectField(
            u'* Type',
            choices=[(u'Client', u'Client'), (u'Enablement', u'Enablement'), (u'Development', u'Development'), (u'Research', u'Research')],
            coerce=unicode,
            validators=[Optional()])

