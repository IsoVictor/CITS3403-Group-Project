# routes.py
from flask_login import UserMixin
from flask import Flask, render_template, request, redirect, url_for, flash, session
from app import app, db, login_manager, login_user
from app.models import User, Post, StudyGroup
from app.flashcard_routes import flashcard_bp
import os
from app.forms import LoginForm, SignupForm



app.register_blueprint(flashcard_bp)

class Question:
    def __init__(self, question_id, question):
        self.question_id = question_id
        self.question = question


allquestions = [
    Question('1','Why does coding make me sad?'),
    Question('2','Why does coding make me happy?'),
    Question('3','Why does coding make me angry?'),
]
# Home page route
@app.route("/")
def index():
    return render_template('index.html')

# Calendar page route
@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

# Questions and answers page route
@app.route('/questions')
def questions():
    return render_template('questions.html')

#Discussion page route
@app.route('/discussion')
def discussion():
    return render_template('discussion.html')

# Study groups page route
@app.route('/study-groups')
def study_groups():
    return render_template('study-groups.html')

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
        
        login_user(user)
        return redirect(url_for('index'))
    
    return render_template('login.html', form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))


# User Answering route
@app.route('/answer/<question_id>', methods=['GET','POST'])
def answer(question_id):
    if request.method == 'GET':
        for question in allquestions:
            if question.question_id == question_id:
                return render_template('answering.html', c_question = question)


#Joining Group route
@app.route('/joingroup/<group_id>', methods=['GET'])
def joingroup(group_id):
    allrelations = UserGroupRelation.query.get(group_id)
    if request.method == 'GET':
        for relation in allreations:
            if relation.user_id == user_id:
                flash('You are already in this group', 'error')
                return redirect(url_for('study_groups'))
            else:
                newrelation = UserGroupRelation()
                newrelation.user_id = user_id
                newrelation.group_id = group_id
                db.session.add(newrelation)
                db.session.commit()
                return redirect(url_for('study_groups'))
                