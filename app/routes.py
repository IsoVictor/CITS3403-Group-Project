from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

#Home page route
@app.route("/")
def index():
    return render_template('index.html')

#Calendar page route
@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

#Flashcards page route
@app.route('/flashcards')
def flashcards():
    return render_template('flashcards.html')

#Questions and answers page route
@app.route('/questions')
def questions():
    return render_template('questions.html')
#Study groups page route
@app.route('/study-groups')
def study_groups():
    return render_template('study-groups.html')
#User registration route
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
        return redirect(url_for('signin'))
    return render_template('signup.html')
#User sigin route
@app.route('/sigin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash('Invalid username or password')
    return render_template('sigin.html')

#User logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))
    

