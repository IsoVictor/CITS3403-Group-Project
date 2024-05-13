from wtfroms import PasswordField, StringField, SubmitField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired])
    password = PasswordField("Password", validators=[DataRequired])
    submit = SubmitField("Login")
    

class SignupForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired])
    studentnumber = StringField("Student Number", validators=[DataRequired])
    username = StringField("Username", validators=[DataRequired])
    password = PasswordField("Password", validators=[DataRequired])
    confirmpassword = PasswordField("Confirm Password", validators=[DataRequired])
    submit = SumbitField("Create Account")