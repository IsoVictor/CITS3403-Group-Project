from app import db
from app.models import User, UserGroupRelation, Post, StudyGroup, Question, Answer
from datetime import datetime

# Sample data for User
user1 = User(username='user1', email='user1@example.com', studentnumber='123456789')
user1.set_password('password1')

user2 = User(username='user2', email='user2@example.com', studentnumber='987654321')
user2.set_password('password2')

# Sample data for Post
post1 = Post(body='This is the first post by user1.', user_id=1, unit_code='CITS3403')
post2 = Post(body='This is the second post by user1.', user_id=1, unit_code='CITS2401')
post3 = Post(body='A post by user2.', user_id=2, unit_code='CITS3403')

# Sample data for StudyGroup
study_group1 = StudyGroup(location='Library', description='Study session for exam', 
                          time=datetime.strptime('13:00', '%H:%M').time(), 
                          date=datetime.strptime('2024-05-15', '%Y-%m-%d').date(), unit_code='CITS3403')
study_group2 = StudyGroup(location='Coffee shop', description='Group project meeting', 
                          time=datetime.strptime('10:30', '%H:%M').time(), 
                          date=datetime.strptime('2024-05-16', '%Y-%m-%d').date(), unit_code='CITS2401')
study_group3 = StudyGroup(location='EZONE', description='Project help', 
                          time=datetime.strptime('13:00', '%H:%M').time(), 
                          date=datetime.strptime('2024-05-15', '%Y-%m-%d').date(), unit_code='CITS3403')

# Sample data for Question
question1 = Question(question='What is the exam format for CITS3403?', unit_code='CITS3403', 
                     user_id=1, posterUsername='user1')
question2 = Question(question='Any tips for the group project in CITS2401?', unit_code='CITS2401', 
                     user_id=2, posterUsername='user2')

# Sample data for Answer
answer1 = Answer(answer='The exam will be a mix of multiple-choice and short-answer questions.', 
                 user_id=2, question_id=1, answerUsername='user2')
answer2 = Answer(answer='Start early and make sure to divide tasks among team members.', 
                 user_id=1, question_id=2, answerUsername='user1')

# Add user group relations after study groups are added to session
user_group_relation1 = UserGroupRelation(user_id=user1.id, group_id=study_group1.group_id)
user_group_relation2 = UserGroupRelation(user_id=user2.id, group_id=study_group1.group_id)
user_group_relation3 = UserGroupRelation(user_id=user1.id, group_id=study_group2.group_id)
user_group_relation4 = UserGroupRelation(user_id=user2.id, group_id=study_group3.group_id)


def add_test_users_to_db():
    db.session.add(user1)
    db.session.add(user2) 
    db.session.commit()


def add_test_posts_to_db():
    db.session.add(post1)
    db.session.add(post2)
    db.session.add(post3)
    db.session.commit()

def add_test_studygroups_to_db():
    db.session.add(study_group1)
    db.session.add(study_group2)
    db.session.add(study_group3)
    db.session.commit()

def add_test_questions_to_db():
    db.session.add(question1)
    db.session.add(question2)
    db.session.commit()

def add_test_answers_to_sb():
    db.session.add(answer1)
    db.session.add(answer2)
    db.session.commit()

def add_test_usergrouprelation_to_db():
    db.session.add(user_group_relation1)
    db.session.add(user_group_relation2)
    db.session.add(user_group_relation3)
    db.session.add(user_group_relation4)
    db.session.commit()


# Add all objects to the session
db.session.add(user1)
db.session.add(user2)

db.session.add(post1)
db.session.add(post2)
db.session.add(post3)

db.session.add(study_group1)
db.session.add(study_group2)
db.session.add(study_group3)

db.session.add(question1)
db.session.add(question2)

db.session.add(answer1)
db.session.add(answer2)

db.session.add(user_group_relation1)
db.session.add(user_group_relation2)
db.session.add(user_group_relation3)
db.session.add(user_group_relation4)

# Commit the changes in one go
db.session.commit()
