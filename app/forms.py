from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, PasswordField,
    FileField, BooleanField, SubmitField)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, Regexp, ValidationError)
from .models import User

# Create the forms in here


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=1, max=50),
    ])
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=25,
            message="Username must be between 4 and 25 characters."),
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Length(min=6, max=35),
        Regexp(
            '^[a-zA-Z0-9.!#$%&*+/=?_~-]+@[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*$',
            message="Must be a valid e-mail"),
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('confirm', message='Passwords do not match'),
    ])
    confirm = PasswordField('Confirm Password')

    submit = SubmitField('Sign Up')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('That username is invalid, please try again')

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('That email is invalid, please try again')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    Password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')


# User Account form class
class UpdateAccountForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=1, max=50),
    ])
    username = StringField('Username', validators=[
        Length(min=4, max=25,
            message="Username must be between 4 and 25 characters."),
    ])
    email = StringField('Email', validators=[
        Length(min=6, max=35),
        Regexp(
            '^[a-zA-Z0-9.!#$%&*+/=?_~-]+@[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*$',
            message="Must be a valid e-mail"),
    ])

    submit = SubmitField('Update')


# Article form class
class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[
        Length(min=1, max=100),
        ])
    body = TextAreaField('Body', validators=[
        Length(min=10)],
        render_kw={'rows': 20})


# Category form class
class CategoryForm(FlaskForm):
    category = StringField('Category', validators=[
        Length(min=3, max=25),
    ])
