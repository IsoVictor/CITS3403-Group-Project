# controllers.py

from datetime import datetime
from app import db
from app.models import StudyGroup, UserGroupRelation, User, Question, UserGroupRelation, Answer
from sqlalchemy import func
from werkzeug.security import check_password_hash
from flask import jsonify, session
from flask_login import current_user

class UserCreationError(Exception):
    pass

def create_user(email, studentnumber, username, password, confirmpassword):
    # Check if passwords match
    if password != confirmpassword:
        raise UserCreationError('Passwords do not match!')

    # Check if email is already registered
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        raise UserCreationError('Email is already registered!')

    # Check if student number is already registered
    existing_student = User.query.filter_by(studentnumber=studentnumber).first()
    if existing_student:
        raise UserCreationError('Student number is already registered!')

    # Check if username is already registered
    existing_student = User.query.filter_by(username = username).first()
    if existing_student:
        raise UserCreationError('Username already registered!')

    # Create new user
    new_user = User(email=email, studentnumber=studentnumber, username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

class GroupJoiningError(Exception):
    pass

def join_group(user_id, group_id):
    # Check if user is already in the group
    existing_relation = UserGroupRelation.query.filter_by(group_id=group_id, user_id=user_id).first()
    if existing_relation:
        raise GroupJoiningError('You are already in this group')

    # Add user to the group
    new_relation = UserGroupRelation(user_id=user_id, group_id=group_id)
    db.session.add(new_relation)
    db.session.commit()


def authenticate_user(username, password):
    # Authenticate user credentials
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None


class StudyGroupCreationError(Exception):
    pass

def create_study_group(unit_code, location, dateof, time, description, user_id):
    # Validate date
    if not dateof or dateof < datetime.today().date():
        raise StudyGroupCreationError('Invalid date. Please select a valid date.')

    # Validate unit code length
    if len(unit_code) != 8:
        raise StudyGroupCreationError('Invalid Unit Code.')

    # Generate new group_id
    max_group_id = db.session.query(func.max(StudyGroup.group_id)).scalar()
    new_group_id = (max_group_id or 0) + 1

    # Create new study group and user-group relation
    new_group = StudyGroup(group_id=new_group_id, unit_code=unit_code, location=location, date=dateof, time=time, description=description)
    new_relation = UserGroupRelation(user_id=user_id, group_id=new_group_id)

    db.session.add(new_relation)
    db.session.add(new_group)
    db.session.commit()

class DiscussionCreationError(Exception):
    pass

def create_discussion(unit_code, question, user_id, poster_username):
    # Validate unit code length
    if len(unit_code) != 8:
        raise StudyGroupCreationError('Invalid Unit Code.')

    # Create new question
    new_question = Question(unit_code=unit_code, question=question, user_id=user_id, posterUsername=poster_username)
    db.session.add(new_question)
    db.session.commit()

class GroupLeavingError(Exception):
    pass

def leave_group(user_id, group_id):
    # Check if user is a member of the group
    relation = UserGroupRelation.query.filter_by(group_id=group_id, user_id=user_id).first()
    if not relation:
        raise GroupLeavingError('You are not a member of this group')

    # Remove user from the group
    db.session.delete(relation)
    db.session.commit()

class AnswerCreationError(Exception):
    pass

def create_answer(answer_text, user_id, question_id, username):
    # Validate answer text
    if not answer_text:
        raise AnswerCreationError('Answer cannot be empty')

    # Create new answer
    new_answer = Answer(answer=answer_text, user_id=user_id, question_id=question_id, answerUsername=username)
    db.session.add(new_answer)
    db.session.commit()

def get_question_and_answers(question_id):
    # Retrieve question and its answers
    question = Question.query.filter_by(id=question_id).first()
    answers = Answer.query.filter_by(question_id=question_id).all()
    return question, answers


def update_profile_controller(form):
    # Update user profile information
    current_user.username = form.username.data
    current_user.firstname = form.firstname.data
    current_user.lastname = form.lastname.data
    current_user.email = form.email.data
    db.session.commit()
    session['username'] = current_user.username
