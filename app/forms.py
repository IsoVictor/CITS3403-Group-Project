from wtforms import PasswordField, StringField, SubmitField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import StringField, TextAreaField, FileField


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
    

class SignupForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    studentnumber = StringField("Student Number", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirmpassword = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Create Account")


class ProfileUpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired()])
    studentnumber = StringField('Student Number', validators=[DataRequired()])
    bio = TextAreaField('Bio')
    profile_picture = FileField('Profile Picture')