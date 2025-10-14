from flask import Flask
from app.models.database import db
from flask_migrate import Migrate
from app.controllers.user_controller import user_bp
from app.controllers.task_controller import task_bp

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:yourpassword@localhost:5432/mydb"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(user_bp)
    app.register_blueprint(task_bp)

    return app
