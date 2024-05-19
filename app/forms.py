from flask import render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TimeField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class SignupForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    studentnumber = StringField("Student Number", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Password", validators=[DataRequired()])
    confirmpassword = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Create Account")



class ProfileUpdateForm(FlaskForm):
    username = StringField('Username', validators=[ Length(min=2, max=64)])
    firstname = StringField('First Name', validators=[ Length(min=2, max=64)])
    lastname = StringField('Last Name', validators=[ Length(min=2, max=64)])
    username = StringField('Username', validators=[ Length(min=2, max=64)])
    email = StringField('Email', validators=[ Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    


class groupForm(FlaskForm):
    unit_code = StringField("Unit Code", validators=[DataRequired(), Length(min = 8, max = 8)])
    location = StringField("Location",validators=[DataRequired()])
    dateof = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    description = StringField('Purpose of Study Group', validators=[DataRequired()])
    submit = SubmitField("Create Group")
    
class questionForm(FlaskForm):
    unit_code = StringField("Unit Code", validators=[DataRequired(), Length(min = 8, max = 8)])
    question = TextAreaField("Question", validators=[DataRequired()])
    submit = SubmitField("Ask Question")

class answerForm(FlaskForm):
    answer = TextAreaField("Answer", validators=[DataRequired()])
    submit = SubmitField("Post Answer")

