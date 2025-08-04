from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
migrate=Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()  # 
mail=Mail() 
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app,db)
    bcrypt.init_app(app)
    login_manager.init_app(app)  
    

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

    with app.app_context():
        from app.models import User, Post
        db.create_all()

    return app
