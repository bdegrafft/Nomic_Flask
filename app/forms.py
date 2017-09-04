from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, validators
from wtforms.validators import DataRequired
from urllib.parse import urlparse, urljoin
from flask import request, url_for


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    # email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(),
    ])
    remember_me = BooleanField('remember_me', default=False)
