from app import db
from flask import current_app
from flask_login import UserMixin
from app import login_manager
from datetime import datetime




class User(db.Model, UserMixin):
    __tablename__='users'
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile_picture = db.Column(db.String(20), nullable=False, default='static/avatars/test.webp')
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"{self.username}({self.email} {self.profile_picture})"

class Post(db.Model,UserMixin):
    __tablename__='posts'
    id=db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(150), nullable=False)
    content= db.Column(db.Text, nullable=False)
    tags=db.Column(db.String(30), nullable=True)
    visibility=db.Column(db.String(10), nullable=False, default='private')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))