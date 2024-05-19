from flask_migrate import Migrate
from app import create_app, db
from app.config import DeploymentConfig

app = create_app(DeploymentConfig)
migrate = Migrate(app, db)