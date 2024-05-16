from flask import render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TimeField
from wtforms.validators import DataRequired

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

class groupForm(FlaskForm):
    unit_code = StringField("Unit Code", validators=[DataRequired()])
    location = StringField("Location",validators=[DataRequired()])
    dateof = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    description = StringField('Purpose of Study Group', validators=[DataRequired()])
    submit = SubmitField("Create Group")
    
class questionForm(FlaskForm):
    unit_code = StringField("Unit Code", validators=[DataRequired()])
    question = StringField("Question", validators=[DataRequired()])
    submit = SubmitField("Ask Question")

class answerForm(FlaskForm):
    answer = StringField("Answer", validators=[DataRequired()])
    submit = SubmitField("Post Question")

    