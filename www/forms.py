import json
from flask.ext.wtf import Form
from wtforms.fields import TextField, TextAreaField, PasswordField
from wtforms.validators import Required, Email, EqualTo


class ComplaintForm(Form):
    email = TextField('Email', validators=[Required(), Email()])
    message = TextAreaField('Feedback', validators=[Required()])

class InviteForm(Form):
    full_name = TextField('Full name', validators=[Required()])
    email = TextField('Email', validators=[Required(), Email()])

class SetPasswordForm(Form):
    password = PasswordField('New Password', [Required(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')
