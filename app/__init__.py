from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler
import os
# Initialize extensions


db = SQLAlchemy()
migrate=Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()  # 
mail=Mail() 

def setup_logging(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/error.log', maxBytes=10240, backupCount=3)
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)


    
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app,db)
    bcrypt.init_app(app)
    login_manager.init_app(app)  
    setup_logging(app)


    #  Configure LoginManager
    login_manager.login_view = 'users.login'  # function name of login route
    login_manager.login_message_category = 'info'  # Bootstrap category for flash messages
    mail.init_app(app)
    from app.users.routes import users
    from app.posts.routes import posts
    from app.main.routes import main
    from app.notes.routes import notes
    from app.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(notes)
    app.register_blueprint(errors)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """Rollback and remove session at the end of the request."""
        if exception:
            db.session.rollback()
        db.session.remove()

    with app.app_context():
        from app.models import User, Post
        db.create_all()

    return app


