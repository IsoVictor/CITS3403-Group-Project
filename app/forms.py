from flask import render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TimeField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    # Field for entering the username
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=50)])
    # Field for entering the password
    password = PasswordField("Password", validators=[DataRequired()])
    # Submit button for the login form
    submit = SubmitField("Login")

class SignupForm(FlaskForm):
    # Field for entering the email address
    email = StringField("Email", validators=[DataRequired()])
    # Field for entering the student number
    studentnumber = StringField("Student Number", validators=[DataRequired()])
    # Field for entering the username
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=50)])
    # Field for entering the password
    password = PasswordField("Password", validators=[DataRequired()])
    # Field for confirming the password
    confirmpassword = PasswordField("Confirm Password", validators=[DataRequired()])
    # Submit button for the signup form
    submit = SubmitField("Create Account")

class ProfileUpdateForm(FlaskForm):
    # Field for updating the username
    username = StringField('Username', validators=[Length(min=2, max=64)])
    # Field for updating the first name
    firstname = StringField('First Name', validators=[Length(min=2, max=64)])
    # Field for updating the last name
    lastname = StringField('Last Name', validators=[Length(min=2, max=64)])
    # Field for updating the email address
    email = StringField('Email', validators=[Email()])
    # Field for uploading a new profile picture (allowed file types: jpg, png)
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    # Submit button for the profile update form
    submit = SubmitField('Update')

class groupForm(FlaskForm):
    # Field for entering the unit code
    unit_code = StringField("Unit Code", validators=[DataRequired(), Length(min=8, max=8)])
    # Field for entering the location of the study group
    location = StringField("Location", validators=[DataRequired()])
    # Field for selecting the date of the study group
    dateof = DateField('Date', validators=[DataRequired()])
    # Field for selecting the time of the study group
    time = TimeField('Time', validators=[DataRequired()])
    # Field for entering the description/purpose of the study group
    description = StringField('Purpose of Study Group', validators=[DataRequired()])
    # Submit button for the study group creation form
    submit = SubmitField("Create Group")

class questionForm(FlaskForm):
    # Field for entering the unit code related to the question
    unit_code = StringField("Unit Code", validators=[DataRequired(), Length(min=8, max=8)])
    # Field for entering the question
    question = TextAreaField("Question", validators=[DataRequired()])
    # Submit button for the question form
    submit = SubmitField("Ask Question")

class answerForm(FlaskForm):
    # Field for entering the answer to a question
    answer = TextAreaField("Answer", validators=[DataRequired()])
    # Submit button for the answer form
    submit = SubmitField("Post Answer")
