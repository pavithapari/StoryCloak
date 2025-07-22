from app import db
from flask import current_app
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile_picture = db.Column(db.String(20), nullable=False, default='static/images/test.webp')
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Post(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(150), nullable=False)
    content= db.Column(db.Text, nullable=False)
    tags=db.Column(db.String(30), nullable=True)
    visibility=db.Column(db.String(10), nullable=False, default='private')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author = db.Column(db.String(150), db.ForeignKey('user.username'), nullable=False)
