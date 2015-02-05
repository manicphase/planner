from wtforms import (
    Form,
    BooleanField,
    StringField,
    IntegerField,
    SelectField,
    TextAreaField
    )
from wtforms.validators import DataRequired, Email


class NewEngagement(Form):
    name = StringField(u'* Name', validators=[DataRequired()])
    client = StringField(u'* Client', validators=[DataRequired()])
    sowlink = StringField(u'* Statement of Works Link',
                          validators=[DataRequired()])
    probability = SelectField(u'* Probability',
                              choices=[('0.0', '0%'), ('0.1', '10%'),
                                       ('0.2', '20%'), ('0.3', '30%'),
                                       ('0.4', '40%'), ('0.5', '50%'),
                                       ('0.6', '60%'), ('0.7', '70%'),
                                       ('0.8', '80%'), ('0.9', '90%'),
                                       ('1.0', '100%')],
                              coerce=str,
                              validators=[DataRequired()])
    sustainability = SelectField(u'* Sustainability',
                                 choices=[('0.1', '10%'), ('0.2', '20%'),
                                          ('0.3', '30%'), ('0.4', '40%'),
                                          ('0.5', '50%'), ('0.6', '60%'),
                                          ('0.7', '70%'), ('0.8', '80%'),
                                          ('0.9', '90%'), ('1.0', '100%')],
                                 coerce=str,
                                 validators=[DataRequired()])
    alignment = SelectField(u'* Alignment',
                            choices=[('0.0', '0%'), ('0.1', '10%'),
                                     ('0.2', '20%'), ('0.3', '30%'),
                                     ('0.4', '40%'), ('0.5', '50%'),
                                     ('0.6', '60%'), ('0.7', '70%'),
                                     ('0.8', '80%'), ('0.9', '90%'),
                                     ('1.0', '100%')],
                            coerce=str,
                            validators=[DataRequired()])
    revenue = IntegerField(u'Revenue Per Iteration')
    status = SelectField(u'* Status',
                         choices=[(u'Complete', u'Complete'),
                                  (u'Sold', u'Sold'),
                                  (u'Negotiation', u'Negotiation'),
                                  (u'Approach', u'Approach'),
                                  (u'Lost', u'Lost')],
                         coerce=str,
                         validators=[DataRequired()])
    complexity = SelectField(u'* Complexity',
                             choices=[('0.1', u'Tiny'), ('0.5', u'Small'),
                                      ('1.0', u'Medium'), ('2.0', u'Large')],
                             coerce=str,
                             validators=[DataRequired()])
    isrnd = BooleanField(u'Eligable for R&D tax credits?')


class NewContact(Form):
    # TODO: More validation
    forename = StringField(u'* Forename', validators=[DataRequired()])
    surname = StringField(u'* Surname', validators=[DataRequired()])
    role = StringField(u'* Role')
    email = StringField(u'* Email', validators=[Email()])
    landline = StringField(u'* Landline')
    mobile = StringField(u'* Mobile')
    address = TextAreaField(u'* Address')
