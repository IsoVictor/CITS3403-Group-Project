# routes.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from app import app, db
from app.models import User, Post, StudyGroup
from app.flashcard_routes import flashcard_bp

app.register_blueprint(flashcard_bp)

class Question:
    def __init__(self, question_id, question):
        self.question_id = question_id
        self.question = question


questions = [
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
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is not None:
            flash('Username already exists.')
            return redirect(url_for('signup'))
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Successfully Registered!')
        return redirect(url_for('login'))
    return render_template('signup.html')

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash('Invalid username or password')
    return render_template('login.html')

# User logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))


# User Answering route
@app.route('/answer/<question_id>', methods=['GET','POST'])
def answer(question_id):
    if request.method == 'GET':
        for question in questions:
            if question.question_id == question_id:
                return render_template('answering.html', c_question = question)

