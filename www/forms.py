import json
from wtforms import Form, TextField, TextAreaField, validators

class ComplaintForm(Form):
    email = TextField('Email', validators=[validators.required('Enter an email address'), validators.Email('Enter a valid email')])
    message = TextAreaField('Message', validators=[validators.required('Enter a message')])
