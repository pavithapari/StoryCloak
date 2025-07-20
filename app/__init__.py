'''We are creating a Flask application with user authentication and database integration.
This code initializes the Flask , sets up the database, bcrypt for password hashing, and login management.
It also imports routes to handle different URL endpoints.This executes when the  is run initializing the  and avoiding circular imports.'''
from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

db=SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail=Mail()





def create_app(config_class=Config):
    app = Flask(__name__)
# Load configuration settings (e.g., development, production) from Config class
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    from app.users.routes import users
    from app.posts.routes import posts
    from app.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    return app


