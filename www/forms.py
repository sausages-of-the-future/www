import json
from wtforms import Form, TextField, TextAreaField, validators

class ComplaintForm(Form):
    email = TextField('Your email address', validators=[validators.required('Enter an email address'), validators.Email('Enter a valid email')])
    message = TextAreaField('Feedback', validators=[validators.required('Enter a message')])
