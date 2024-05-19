from unittest import TestCase

from app import create_app, db
from app.config import TestConfig
from app.controllers import UserCreationError, create_user, authenticate_user, create_study_group, StudyGroupCreationError, create_discussion, DiscussionCreationError, join_group, GroupJoiningError, leave_group, GroupLeavingError, AnswerCreationError, create_answer, get_question_and_answers
from app.models import User, UserGroupRelation

class BasicUnitTests(TestCase):

    def setUp(self):
        testApp = create_app(TestConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    #Tests for the sign up aspect out of application

    def test_sign_up_different_passwords(self):
        with self.assertRaisesRegex(UserCreationError,'Passwords do not match!'):
            create_user('test@example.com', '123456789', 'test_user', 'password1', 'password2')

    def test_sign_up_same_username(self):
        existing_user = User(username='user1', email='user1@example.com', studentnumber = '1235678')
        db.session.add(existing_user)
        db.session.commit()
        with self.assertRaisesRegex(UserCreationError,'Username already registered!'):
            create_user('test@example.com', '123456789', 'user1', 'password1', 'password1')

    
    def test_sign_up_same_studentNumber(self):
        existing_user = User(username='user1', email='user1@example.com', studentnumber = '12345678')
        db.session.add(existing_user)
        db.session.commit()
        with self.assertRaisesRegex(UserCreationError,'Student number is already registered!'):
            create_user('test@example.com', '12345678', 'user1', 'password1', 'password1')


    def test_sign_up_same_email(self):
        existing_user = User(username='user1', email='user1@example.com', studentnumber = '12345678')
        db.session.add(existing_user)
        db.session.commit()
        with self.assertRaisesRegex(UserCreationError,'Email is already registered!'):
            create_user('user1@example.com', '123456789', 'user1', 'password1', 'password1')

    def test_sign_up_successfull(self):
        existing_user = User(username='user2', email='user2@example.com', studentnumber = '23456789')
        db.session.add(existing_user)
        db.session.commit()
        try:
            create_user('user1@example.com', '12345678', 'user1', 'password1', 'password1')
        except UserCreationError as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_password_hashing(self):
        existing_user = User(username='user1', email='user1@example.com', studentnumber='12345678')
        existing_user.set_password("password1")
        self.assertTrue(existing_user.check_password('password1'))
        self.assertFalse(existing_user.check_password('password2'))

    #Test for joining and leaving groups
    def test_joining_already_joined_group(self):
        your_id = 1
        existing_group_id = 1
        existing_relationship = UserGroupRelation(user_id = your_id, group_id=existing_group_id)
        db.session.add(existing_relationship)
        db.session.commit()
        with self.assertRaisesRegex(GroupJoiningError,'You are already in this group'):
            join_group(your_id, existing_group_id)

    def test_joining_new_group(self):
        your_id = 1
        existing_group1_id = 1
        existing_group2_id = 2
        existing_relationship = UserGroupRelation(user_id = your_id, group_id = existing_group1_id)
        db.session.add(existing_relationship)
        db.session.commit()
        try:
            join_group(your_id, existing_group2_id)
        except GroupJoiningError as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_leaving_group_not_in(self):
        your_id = 1
        not_your_group = 1
        your_group = 2
        existing_relationship = UserGroupRelation(user_id = your_id, group_id = your_group)
        db.session.add(existing_relationship)
        db.session.commit()
        with self.assertRaisesRegex(GroupLeavingError,'You are not a member of this group'):
            leave_group(your_id, not_your_group)

    def test_leaving_your_group(self):
        your_id = 1
        your_group = 1
        existing_relationship = UserGroupRelation(user_id = your_id, group_id = your_group)
        db.session.add(existing_relationship)
        db.session.commit()
        try:
            leave_group(your_id, your_group)
        except GroupLeavingError as e:
            self.fail(f"Unexpected exception raised: {e}")
