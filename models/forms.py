#!venv/bin/python3
""" Form module """
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from agent_app import db
from models.user import User
from models.agent import Agent

user = object

class LoginForm(FlaskForm):
    """ Login form class """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    user_type = StringField('Customer or Agent ?', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class EditProfileForm(FlaskForm):
    """ Edit profile class """
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            agent = db.session.scalar(sa.select(Agent).where(
                Agent.username == username.data))
            if agent is not None:
                raise ValidationError('Please use a different agentname.')


class RegistrationForm(FlaskForm):
    """ Registration class """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    user_type = StringField('Customer or Agent ?', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        # if (self.user_type.data == "Customer" or "customer"):
        #     user = db.session.scalar(sa.select(User).where(
        #         User.username == username.data))
        # else:
        user = db.session.scalar(sa.select(Agent).where(
            Agent.username == username.data))
        if user is not None:
            raise ValidationError('User already registered, please use a different username.')

    def validate_email(self, email):
        # if (self.user_type.data == 'Customer' or 'customer'):
        #     user = db.session.scalar(sa.select(User).where(
        #         User.email == email.data))
        # else:
        user = db.session.scalar(sa.select(Agent).where(
                Agent.email == email.data))
        if user is not None:
            raise ValidationError('Email already exist use different email.')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    post = TextAreaField('Post property', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')