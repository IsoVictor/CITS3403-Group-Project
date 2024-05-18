# routes.py
from flask_login import UserMixin, current_user, login_required, login_user, logout_user
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from app.models import User, Post, StudyGroup, UserGroupRelation, Question, Answer
import os
from app.forms import LoginForm, SignupForm, groupForm, answerForm, questionForm, ProfileUpdateForm
from sqlalchemy import func
from app.blueprints import main
from app.controllers import UserCreationError, create_user, authenticate_user, create_study_group, StudyGroupCreationError, create_discussion, DiscussionCreationError, join_group, GroupJoiningError, leave_group, GroupLeavingError
from datetime import datetime


# Home page route
@main.route("/")
def index():
    return render_template('index.html')

# Calendar page route
@main.route('/calendar')
@login_required
def calendar():
    user_id = current_user.id
    study_group_events = []
    user_groups = UserGroupRelation.query.filter_by(user_id=user_id).all()
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
    return render_template('calendar.html', study_group_events=study_group_events)

@main.route('/add-event', methods=['POST'])
def add_event():
    title = request.json['title']
    date = request.json['date']
    event = Event(title=title, date=date, user_id=current_user.id)
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Event added successfully'})

@main.route('/delete-event', methods=['POST'])
def delete_event():
    event_id = request.json['eventId']
    event = Event.query.filter_by(id=event_id, user_id=current_user.id).first()
    if event:
        db.session.delete(event)
        db.session.commit()
        return jsonify({'message': 'Event deleted successfully'})
    return jsonify({'error': 'Event not found'})

@main.route('/edit-event/<int:event_id>', methods=['PUT'])
def edit_event(event_id):
    event = Event.query.filter_by(id=event_id, user_id=current_user.id).first()
    if event:
        event.title = request.json['title']
        event.date = request.json['date']
        db.session.commit()
        return jsonify({'message': 'Event updated successfully'})
    return jsonify({'error': 'Event not found'})

@main.route('/discussion', methods=["GET", "POST"])
def discussion():
    form = questionForm()
    allquestions = Question.query.all()
    
    if request.method == "POST" and form.validate_on_submit():
        unit_code = form.unit_code.data
        question = form.question.data
        user_id = current_user.id

        try:
            create_discussion(unit_code, question, user_id, current_user.username)
            flash('Discussion created successfully!', 'success')
            return redirect(url_for('main.discussion'))
        except DiscussionCreationError as e:
            flash(str(e), 'error')

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
            create_study_group(unit_code, location, dateof, time, description, current_user.id)
            flash('Group created successfully!', 'success')
            return redirect(url_for('main.study_groups'))
        except StudyGroupCreationError as e:
            flash(str(e), 'error')

    return render_template('study-groups.html', form=form, allgroups=allgroups)


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if not form.validate_on_submit():
        return render_template('signup.html', form=form)

    email = form.email.data
    studentnumber = form.studentnumber.data
    username = form.username.data
    password = form.password.data
    confirmpassword = form.confirmpassword.data
    #testing blueprint
    try:
        create_user(email, studentnumber, username, password, confirmpassword)
    except UserCreationError as e:
        flash(str(e), 'error')
        return redirect(url_for('main.signup'))

    flash('Account created successfully!', 'success')
    return redirect(url_for('main.login'))
      # Pass the form to the template


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if not form.validate_on_submit():
        return  render_template('login.html', form=form)
    
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


# User Answering route
@main.route('/answer/<question_id>', methods=['GET','POST'])
@login_required
def answer(question_id):
    form = answerForm()
    answers = Answer.query.filter_by(question_id=question_id).all()
    question = Question.query.filter_by(id=question_id).first()
    if form.validate_on_submit():
        answer = form.answer.data
        new_answer = Answer(answer = answer, user_id = current_user.id, question_id = question_id, answerUsername = current_user.username)
        db.session.add(new_answer)
        db.session.commit()
        return redirect(url_for('main.answer',question_id = question_id))
        
    return render_template('answering.html', question= question, answers = answers, form = form)


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileUpdateForm()

    if form.validate_on_submit():
        # Update user data with form data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.studentnumber = form.studentnumber.data
        # Save profile picture if uploaded
        if profile_pic:
            filename = secure_filename(profile_pic.filename)
            photos.save(profile_pic, name=filename)
            user.profile_pic = filename
        # Commit changes to the database
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))

    # Pre-populate form fields with current user data
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.studentnumber.data = current_user.studentnumber

    return render_template('user-profile.html', form=form, user=current_user)
    
@main.route('/joingroup/<group_id>', methods=['GET'])
@login_required
def joingroup(group_id):
    try:
        join_group(current_user.id, group_id)
        flash('You have successfully joined the group!', 'success')
    except GroupJoiningError as e:
        flash(str(e), 'error')

    return redirect(url_for('main.study_groups'))
                

@main.route('/leavegroup/<group_id>', methods=['POST'])
@login_required
def leavegroup(group_id):
    try:
        leave_group(current_user.id, group_id)
        flash('You have successfully left the group!', 'success')
    except GroupLeavingError as e:
        flash(str(e), 'error')

    return redirect(url_for('main.study_groups'))