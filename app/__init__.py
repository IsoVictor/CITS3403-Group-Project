from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///study_app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(flaskApp)
login.login_view = 'login'

app.debug = True

from app import routes