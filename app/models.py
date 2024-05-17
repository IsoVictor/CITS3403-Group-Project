

# models.py
from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime




class UserGroupRelation(db.Model):
     __tablename__ = 'user_group_relation'
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True) 
     group_id = db.Column(db.Integer, db.ForeignKey('study_group.group_id'), primary_key=True)
     user = db.relationship("User", back_populates="group_relations", foreign_keys=[user_id]) 
     group = db.relationship("StudyGroup", back_populates="user_relations", foreign_keys=[group_id])




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    studentnumber = db.Column(db.String(10), index=True, unique=True) 
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    flashcard_sets = db.relationship('FlashcardSet', backref='user', lazy='dynamic')
    profilepic = db.Column(db.String(128), nullable=True)
    group_relations = db.relationship('UserGroupRelation', back_populates='user')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_active(self):
        return self.active

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    unit_code = db.Column(db.String(8), nullable=False)

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class StudyGroup(db.Model):
    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    time = db.Column(db.Time)
    date = db.Column(db.Date)
    user_relations = db.relationship("UserGroupRelation", back_populates='group')
    unit_code = db.Column(db.String(8), nullable=False)
    

    def __repr__(self):
        return '<StudyGroup {}>'.format(self.group_id)

class FlashcardSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flashcards = db.relationship('Flashcard', backref='flashcard_set', lazy='dynamic')

class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(200), nullable=False)
    flashcard_set_id = db.Column(db.Integer, db.ForeignKey('flashcard_set.id'), nullable=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    unit_code = db.Column(db.String(8), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    posterUsername = db.Column(db.String(100), nullable=False)
    answers = db.relationship('Answer', backref='question', lazy='dynamic')

    def __repr__(self):
        return '<Question {}>'.format(self.id)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text, nullable=False)  # No limit
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answerUsername = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Answer {}>'.format(self.id)


