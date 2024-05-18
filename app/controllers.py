# controllers.py

from datetime import datetime
from app import db
from app.models import StudyGroup, UserGroupRelation, User, Question, UserGroupRelation
from sqlalchemy import func
from werkzeug.security import check_password_hash

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

class GroupJoiningError(Exception):
    pass

def join_group(user_id, group_id):
    existing_relation = UserGroupRelation.query.filter_by(group_id=group_id, user_id=user_id).first()
    if existing_relation:
        raise GroupJoiningError('You are already in this group')

    new_relation = UserGroupRelation(user_id=user_id, group_id=group_id)
    db.session.add(new_relation)
    db.session.commit()


def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None


class StudyGroupCreationError(Exception):
    pass

def create_study_group(unit_code, location, dateof, time, description, user_id):
    if not dateof or dateof < datetime.today().date():
        raise StudyGroupCreationError('Invalid date. Please select a valid date.')

    # Handles the group_id assignment
    max_group_id = db.session.query(func.max(StudyGroup.group_id)).scalar()
    new_group_id = (max_group_id or 0) + 1

    new_group = StudyGroup(group_id=new_group_id, unit_code=unit_code, location=location, date=dateof, time=time, description=description)
    new_relation = UserGroupRelation(user_id=user_id, group_id=new_group_id)

    db.session.add(new_relation)
    db.session.add(new_group)
    db.session.commit()

class DiscussionCreationError(Exception):
    pass

def create_discussion(unit_code, question, user_id, poster_username):
    new_question = Question(unit_code=unit_code, question=question, user_id=user_id, poster_username=poster_username)
    db.session.add(new_question)
    db.session.commit()

class GroupLeavingError(Exception):
    pass

def leave_group(user_id, group_id):
    relation = UserGroupRelation.query.filter_by(group_id=group_id, user_id=user_id).first()
    if not relation:
        raise GroupLeavingError('You are not a member of this group')

    db.session.delete(relation)
    db.session.commit()