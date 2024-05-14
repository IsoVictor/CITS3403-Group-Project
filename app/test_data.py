from app import db
from app.models import *

# Sample data for UserGroupRelation
user_group_relation1 = UserGroupRelation(user_id=1, group_id=1)
user_group_relation2 = UserGroupRelation(user_id=2, group_id=1)

# Sample data for User
user1 = User(id = 1, username='user1', email='user1@example.com', studentnumber='123456789')
user1.set_password('password1')

user2 = User(id = 2, username='user2', email='user2@example.com', studentnumber='987654321')
user2.set_password('password2')

# Sample data for Post
post1 = Post(body='This is the first post by user1.', user_id=1, unit_code = 'CITS3403')
post2 = Post(body='This is the second post by user1.', user_id=1, unit_code = 'CITS2401')
post3 = Post(body='A post by user2.', user_id=2, unit_code = 'CITS3403')

# Sample data for StudyGroup
study_group1 = StudyGroup(group_id = 1, location='Library', description='Study session for exam', time=datetime.strptime('13:00', '%H:%M').time(), date=datetime.strptime('2024-05-15', '%Y-%m-%d').date(), unit_code = 'CITS3403')
study_group2 = StudyGroup(group_id = 2,location='Coffee shop', description='Group project meeting', time=datetime.strptime('10:30', '%H:%M').time(), date=datetime.strptime('2024-05-16', '%Y-%m-%d').date(), unit_code = 'CITS2401')
study_group3 = StudyGroup(group_id = 3, location='EZONE', description='Project help', time=datetime.strptime('13:00', '%H:%M').time(), date=datetime.strptime('2024-05-15', '%Y-%m-%d').date(), unit_code = 'CITS3403')

# Add data to the session
db.session.add(user_group_relation1)
db.session.add(user_group_relation2)
db.session.add(user1)
db.session.add(user2)
db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.add(study_group1)
db.session.add(study_group2)

# Commit the changes
db.session.commit()