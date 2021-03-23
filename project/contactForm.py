from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, validators
from wtforms.fields.html5 import EmailField


class ContactForm(Form):
    name = StringField("Name", [validators.DataRequired()])
    email = EmailField("Email", [validators.DataRequired()])
    subject = StringField("Subject", [validators.DataRequired()])
    message = TextAreaField("Message", [validators.DataRequired()])
    submit = SubmitField("Send")

