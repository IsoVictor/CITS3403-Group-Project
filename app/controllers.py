# controllers.py

from app.models import User
from app import db

class UserCreationError(Exception):
    pass

def create_user(email, studentnumber, username, password, confirmpassword):
    if password != confirmpassword:
        raise UserCreationError('Passwords do not match!')

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        raise UserCreationError('Email is already registered!')

    existing_student = User.query.filter_by(studentnumber=studentnumber).first()
    if existing_student:
        raise UserCreationError('Student number is already registered!')

    new_user = User(email=email, studentnumber=studentnumber, username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
