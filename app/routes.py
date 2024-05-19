# routes.py
from flask_login import UserMixin, current_user, login_required, logout_user
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
from app import app, db, login_manager, login_user
from app.models import User, Post, StudyGroup, UserGroupRelation, Question, Answer
import os
from app.forms import LoginForm, SignupForm, groupForm, answerForm, questionForm, ProfileUpdateForm
import secrets
from PIL import Image
from datetime import datetime
from sqlalchemy import func

# Home page route
@app.route("/")
def index():
    return render_template('index.html')

# Calendar page route
@app.route('/calendar')
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

@app.route('/add-event', methods=['POST'])
def add_event():
    title = request.json['title']
    date = request.json['date']
    event = Event(title=title, date=date, user_id=current_user.id)
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Event added successfully'})

@app.route('/delete-event', methods=['POST'])
def delete_event():
    event_id = request.json['eventId']
    event = Event.query.filter_by(id=event_id, user_id=current_user.id).first()
    if event:
        db.session.delete(event)
        db.session.commit()
        return jsonify({'message': 'Event deleted successfully'})
    return jsonify({'error': 'Event not found'})

@app.route('/edit-event/<int:event_id>', methods=['PUT'])
def edit_event(event_id):
    event = Event.query.filter_by(id=event_id, user_id=current_user.id).first()
    if event:
        event.title = request.json['title']
        event.date = request.json['date']
        db.session.commit()
        return jsonify({'message': 'Event updated successfully'})
    return jsonify({'error': 'Event not found'})

# discussion and answers page route
@app.route('/discussion', methods=["GET","POST"])
def discussion():
    form = questionForm()
    allquestions = Question.query.all()

    if form.validate_on_submit():
        unit_code = form.unit_code.data
        question = form.question.data
        user_id = current_user.id

        new_question = Question(unit_code = unit_code, question= question, user_id = user_id, posterUsername = current_user.username)
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('discussion'))

    return render_template('discussion.html', form=form, allquestions=allquestions)

# Study groups page route
@app.route('/study-groups', methods=["GET",'POST'])
def study_groups():
    form = groupForm()
    allgroups = StudyGroup.query.all()

    if form.validate_on_submit():
        unit_code = form.unit_code.data
        location = form.location.data
        dateof = form.dateof.data
        time = form.time.data
        description = form.description.data

        # Check if dateof is before the current date
        if dateof < datetime.today().date():
            flash('Date cannot be before the current date.', 'error')
            return redirect(url_for('study_groups'))

        #handles the group_id assignment since automatic handling via SQL_Alchemy wasn't working returning not NULL error
        max_group_id = db.session.query(func.max(StudyGroup.group_id)).scalar()
        new_group_id = (max_group_id or 0) + 1
        
        new_group = StudyGroup(group_id=new_group_id, unit_code=unit_code, location=location, date=dateof, time=time, description=description)
        new_relation = UserGroupRelation(user_id=current_user.id, group_id=new_group_id)
        
        db.session.add(new_relation)
        db.session.add(new_group)
        db.session.commit()
        
        flash('Group created successfully!', 'success')
        return redirect(url_for('study_groups'))
    
    return render_template('study-groups.html', form = form, allgroups = allgroups)

# User registration route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()  # Create an instance of the SignupForm

    if form.validate_on_submit():  # Check if the form is submitted and valid
        email = form.email.data
        studentnumber = form.studentnumber.data
        username = form.username.data
        password = form.password.data
        confirmpassword = form.confirmpassword.data
        
        # Check if passwords match
        if password != confirmpassword:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('signup'))
        
        # Check if email is already registered
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already registered!', 'error')
            return redirect(url_for('signup'))
        
        # Check if student number is already registered
        existing_student = User.query.filter_by(studentnumber=studentnumber).first()
        if existing_student:
            flash('Student number is already registered!', 'error')
            return redirect(url_for('signup'))
        
        # Create new user
        new_user = User(email=email, studentnumber=studentnumber, username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html', form=form)  # Pass the form to the template


# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if not user:
            flash(f'No account found with username {username}', 'error')
            return redirect(url_for('login'))
        
        password = form.password.data
        if not user.check_password(password):
            flash(f'Invalid password. Please try again.', 'error')
            return redirect(url_for('login'))
        
        session['username'] = user.username
        
        login_user(user)
        return redirect(url_for('index'))
    
    return render_template('login.html', form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User logout route
@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('index'))


# User Answering route
@app.route('/answer/<question_id>', methods=['GET','POST'])
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
        return redirect(url_for('answer',question_id = question_id))
    return render_template('answering.html', question= question, answers = answers, form = form)

@app.route('/profile', methods=['GET'])
@login_required
def profile():
    form = ProfileUpdateForm()
    profilepic = url_for('static', filename='profile_pics/' + (current_user.profilepic if current_user.profilepic else 'default.jpg'))

    return render_template('user-profile.html', form=form, profilepic=profilepic, user=current_user)

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    form = ProfileUpdateForm()
    allusers = User.query.all()
    if form.validate_on_submit():
    
        current_user.username = form.username.data
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data
        if form.picture.data:
            picture_file = upload_profile_picture(form.picture.data)
            current_user.profilepic = picture_file

        db.session.commit()
                # Return JSON indicating success
        return jsonify({'success': True,
                        'firstname': current_user.firstname,
                        'lastname': current_user.lastname,
                        'email': current_user.email,
                        'username': current_user.username})
    else:
        # Return JSON indicating failure and errors
        errors = form.errors
        return jsonify({'success': False,
                        'errors': errors})

@app.route('/upload_profile_picture', methods=['POST'])
@login_required
def upload_profile_picture():
    picture_file = request.files['profile_picture']
    if picture_file:
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(picture_file.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

        output_size = (125, 125)
        i = Image.open(picture_file)
        i.thumbnail(output_size)
        i.save(picture_path)
        current_user.profilepic = picture_fn
        db.session.commit()
        return redirect(url_for('profile'))
    return 'No file provided', 400

#Joining Group route
@app.route('/joingroup/<group_id>', methods=['GET'])
@login_required
def joingroup(group_id):
    existing_relation = UserGroupRelation.query.filter_by(group_id=group_id, user_id=current_user.id).first()
    if request.method == 'GET':
        if existing_relation:
            flash('You are already in this group', 'error')
            return redirect(url_for('study_groups'))
            
        new_relation = UserGroupRelation()
        new_relation.user_id = current_user.id
        new_relation.group_id = group_id
        db.session.add(new_relation)
        db.session.commit()
        flash('You have successfully joined the group!', 'success')
        return redirect(url_for('study_groups'))
                
# Leave Group route
@app.route('/leavegroup/<group_id>', methods=['POST'])
@login_required
def leavegroup(group_id):
    relation = UserGroupRelation.query.filter_by(group_id=group_id, user_id=current_user.id).first()
    if relation:
        db.session.delete(relation)
        db.session.commit()
        flash('You have successfully left the group!', 'success')
    else:
        flash('You are not a member of this group!', 'error')
    return redirect(url_for('study_groups'))
