from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms import validators


class LoginForm(Form):
    username = StringField(u'Username', validators=[validators.required()])
    password = PasswordField(u'Password', validators=[validators.optional()])
