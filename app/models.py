from app import db, login_manager
from flask import current_app
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer

# --------------------- User Model ---------------------
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile_picture = db.Column(db.String(20), nullable=False, default='static/avatars/test.webp')
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    posts = db.relationship('Post', backref='author', lazy=True)
    likes = db.relationship('Like', back_populates='user', cascade="all, delete-orphan")
    private_notes = db.relationship('PrivateNote', back_populates='author', cascade='all, delete-orphan')

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

# --------------------- Post Model ---------------------
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(30), nullable=True)
    visibility = db.Column(db.String(10), nullable=False, default='private')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    likes = db.relationship('Like', back_populates='post', cascade="all, delete-orphan")

# --------------------- Like Model ---------------------
class Like(db.Model):
    __tablename__ = 'like_table'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='likes')
    post = db.relationship('Post', back_populates='likes')

# --------------------- PrivateNote Model ---------------------
class PrivateNote(db.Model):
    __tablename__ = 'private_notes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    visibility = db.Column(db.String(10), nullable=False, default='private')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ✅ Only one relationship to User to avoid conflict
    author = db.relationship('User', back_populates='private_notes')

# --------------------- Login Loader ---------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))