"""Forms used by Interview Coach."""

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=128)])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class AnswerForm(FlaskForm):
    answer = TextAreaField('Your answer', validators=[DataRequired(), Length(min=30, max=5000)])


class GuestLoginForm(FlaskForm):
    """CSRF-protected form for starting a guest session."""

    submit = SubmitField('Continue as guest')
