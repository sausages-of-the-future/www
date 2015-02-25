import json
from flask.ext.wtf import Form
from wtforms.fields import TextField, TextAreaField
from wtforms.validators import Required, Email


class ComplaintForm(Form):
    email = TextField('Email', validators=[Required(), Email()])
    message = TextAreaField('Feedback', validators=[Required()])

class InviteForm(Form):
    full_name = TextField('Full name', validators=[Required()])
    email = TextField('Email', validators=[Required(), Email()])
