# routes.py
from flask_login import UserMixin, current_user, login_required, login_user, logout_user
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from app.models import User, Post, StudyGroup, UserGroupRelation, Question, Answer
import os
from app.forms import LoginForm, SignupForm, groupForm, answerForm, questionForm, ProfileUpdateForm
from sqlalchemy import func
from PIL import Image
from app.blueprints import main
import secrets
from app.controllers import UserCreationError, create_user, authenticate_user, create_study_group, StudyGroupCreationError, create_discussion, DiscussionCreationError, join_group, GroupJoiningError, leave_group, GroupLeavingError, create_answer, get_question_and_answers, AnswerCreationError, update_profile_controller
from datetime import datetime
from sqlalchemy import func

# Home page route
@main.route("/")
def index():
    # Render the index.html template
    return render_template('index.html')

# Calendar page route
@main.route('/calendar')
@login_required
def calendar():
    user_id = current_user.id
    study_group_events = []
    
    # Retrieve the user's study groups
    user_groups = UserGroupRelation.query.filter_by(user_id=user_id).all()
    
    # Prepare the study group events data for the calendar
    for user_group in user_groups:
        study_group = StudyGroup.query.filter_by(group_id=user_group.group_id).first()
        if study_group:
            study_group_events.append({
                'title': f"{study_group.unit_code} - {study_group.description}",
                'start': study_group.date.isoformat(),
                'extendedProps': {
                    'location': study_group.location,
                    'time': study_group.time.strftime("%H:%M")
                }
            })
    
    # Render the calendar.html template with the study group events data
    return render_template('calendar.html', study_group_events=study_group_events)


@main.route('/discussion', methods=["GET", "POST"])
def discussion():
    form = questionForm()
    allquestions = Question.query.all()
    
    if request.method == "POST" and form.validate_on_submit():
        unit_code = form.unit_code.data
        question = form.question.data
        user_id = current_user.id
        
        try:
            # Create a new discussion using the provided data
            create_discussion(unit_code, question, user_id, current_user.username)
            flash('Discussion created successfully!', 'success')
            return redirect(url_for('main.discussion'))
        except DiscussionCreationError as e:
            flash(str(e), 'error')
    
    # Render the discussion.html template with the form and all questions
    return render_template('discussion.html', form=form, allquestions=allquestions)



@main.route('/study-groups', methods=["GET", 'POST'])
def study_groups():
    form = groupForm()
    allgroups = StudyGroup.query.all()
    
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Please fill out the form correctly.', 'error')
            return render_template('study-groups.html', form=form, allgroups=allgroups)
        
        unit_code = form.unit_code.data
        location = form.location.data
        dateof = form.dateof.data
        time = form.time.data
        description = form.description.data
        
        try:
            # Create a new study group using the provided data
            create_study_group(unit_code, location, dateof, time, description, current_user.id)
            flash('Group created successfully!', 'success')
            return redirect(url_for('main.study_groups'))
        except StudyGroupCreationError as e:
            flash(str(e), 'error')
    
    # Render the study-groups.html template with the form and all groups
    return render_template('study-groups.html', form=form, allgroups=allgroups)


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    
    if not form.validate_on_submit():
        # Render the signup.html template with the form if form validation fails
        return render_template('signup.html', form=form)
    
    email = form.email.data
    studentnumber = form.studentnumber.data
    username = form.username.data
    password = form.password.data
    confirmpassword = form.confirmpassword.data
    
    try:
        # Create a new user using the provided data
        create_user(email, studentnumber, username, password, confirmpassword)
    except UserCreationError as e:
        flash(str(e), 'error')
        return redirect(url_for('main.signup'))
    
    flash('Account created successfully!', 'success')
    return redirect(url_for('main.login'))


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if not form.validate_on_submit():
        # Render the login.html template with the form if form validation fails
        return render_template('login.html', form=form)
    
    username = form.username.data
    user = User.query.filter_by(username=username).first()
    
    if not user:
        flash(f'No account found with username {username}', 'error')
        return redirect(url_for('main.login'))
    
    password = form.password.data
    if not user.check_password(password):
        flash(f'Invalid password. Please try again.', 'error')
        return redirect(url_for('main.login'))
    
    session['username'] = user.username
    login_user(user)
    return redirect(url_for('main.index'))


# User logout route
@main.route('/logout')
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@main.route('/answer/<question_id>', methods=['GET', 'POST'])
@login_required
def answer(question_id):
    form = answerForm()
    question, answers = get_question_and_answers(question_id)
    
    if not form.validate_on_submit():
        if form.errors:
            for error_field, error_messages in form.errors.items():
                for error in error_messages:
                    flash(f"{error_field}: {error}", 'error')
    else:
        answer_text = form.answer.data
        try:
            # Create a new answer using the provided data
            create_answer(answer_text, current_user.id, question_id, current_user.username)
            return redirect(url_for('main.answer', question_id=question_id))
        except AnswerCreationError as e:
            flash(str(e), 'error')
    
    # Render the answering.html template with the question, answers, and form
    return render_template('answering.html', question=question, answers=answers, form=form)


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileUpdateForm()
    # Render the user-profile.html template with the form and current user
    return render_template('user-profile.html', form=form, user=current_user)


@main.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    form = ProfileUpdateForm()
    if form.validate_on_submit():
        # Update the user's profile using the provided form data
        update_profile_controller(form)
        return jsonify({'success': True,
                        'firstname': current_user.firstname,
                        'lastname': current_user.lastname,
                        'email': current_user.email,
                        'username': current_user.username})
    else:
        errors = form.errors
        return jsonify({'success': False,
                        'errors': errors})


# Joining Group route
@main.route('/joingroup/<group_id>', methods=['GET'])
@login_required
def joingroup(group_id):
    try:
        # Join the group with the provided group_id
        join_group(current_user.id, group_id)
        flash('You have successfully joined the group!', 'success')
    except GroupJoiningError as e:
        flash(str(e), 'error')
    
    return redirect(url_for('main.study_groups'))


@main.route('/leavegroup/<group_id>', methods=['POST'])
@login_required
def leavegroup(group_id):
    try:
        # Leave the group with the provided group_id
        leave_group(current_user.id, group_id)
        flash('You have successfully left the group!', 'success')
    except GroupLeavingError as e:
        flash(str(e), 'error')
    
    return redirect(url_for('main.study_groups'))
