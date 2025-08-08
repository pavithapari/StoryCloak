from app import db, login_manager
from flask import current_app
from flask_login import UserMixin

from itsdangerous import URLSafeTimedSerializer as Serializer
from sqlalchemy.sql import func
from datetime import timedelta

# --------------------- User Model ---------------------
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile_picture = db.Column(db.String(200), nullable=False, default='https://api.dicebear.com/9.x/fun-emoji/svg?seed=Eliza')
    date_joined = db.Column(db.DateTime, nullable=False, default=func.now())
    is_confirmed = db.Column(db.Boolean, default=False)  
    posts = db.relationship('Post', backref='author', lazy=True)
    likes = db.relationship('Like', back_populates='user', cascade="all, delete-orphan")
    private_notes = db.relationship('PrivateNote', back_populates='author', cascade='all, delete-orphan')
    saved_posts = db.relationship('SavePost', back_populates='user', cascade='all, delete-orphan')

    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})
    
    

    @staticmethod
    def verify_reset_token(token, expires_sec=360):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=expires_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile_picture}')"

    def get_confirm_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_confirm_token(token, expires_sec=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=expires_sec)['user_id']
        except Exception:
            return None
        return User.query.get(user_id)

# --------------------- Post Model ---------------------
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(30), nullable=True)
    visibility = db.Column(db.String(10), nullable=False, default='private')
    date_posted = db.Column(db.DateTime, nullable=False, default=func.timezone('Asia/Kolkata', func.now()))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    saved_by_users = db.relationship('SavePost', back_populates='post', cascade="all, delete-orphan")
    likes = db.relationship('Like', back_populates='post', cascade="all, delete-orphan")

# --------------------- Like Model ---------------------
class Like(db.Model):
    __tablename__ = 'like_table'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id',ondelete='CASCADE'))
    timestamp = db.Column(db.DateTime, default=func.now())

    user = db.relationship('User', back_populates='likes')
    post = db.relationship('Post', back_populates='likes')


# --------------------- PrivateNote Model ---------------------
class PrivateNote(db.Model):
    __tablename__ = 'private_notes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    visibility = db.Column(db.String(10), nullable=False, default='private')
    created_at = db.Column(db.DateTime, default=func.timezone('Asia/Kolkata', func.now()))
    updated_at = db.Column(db.DateTime, default=func.timezone('Asia/Kolkata', func.now()), onupdate=func.timezone('Asia/Kolkata', func.now()))

    # ✅ Only one relationship to User to avoid conflict
    author = db.relationship('User', back_populates='private_notes')


# --------------------- save posts model --------------------
class SavePost(db.Model):
    __tablename__ = 'saved_posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'), nullable=False)
    post_id=db.Column(db.Integer, db.ForeignKey('posts.id',ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='saved_posts')
    post = db.relationship('Post', back_populates='saved_by_users')




# --------------------- Login Loader ---------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))