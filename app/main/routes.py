from flask import Blueprint

from flask import render_template, request
from app import db
from flask_login import current_user
from sqlalchemy import func
from datetime import datetime
from app.models import Post
from app.models import User,Like

main = Blueprint('main', __name__)



@main.route("/_ping")
def ping():
    return "OK", 200

@main.route('/')
def home():
    current_year = datetime.now().year
    page=request.args.get('page', 1, type=int) 
    trending_posts = db.session.query(Post, func.count(Like.id).label('like_count'))\
        .outerjoin(Like, Post.id == Like.post_id)\
        .group_by(Post.id)\
        .order_by(func.count(Like.id).desc())\
        .limit(5).all()
    top_5=[post for post,like in trending_posts]
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=4) 
    return render_template('home.html', now=datetime.now(), year=current_year,user=current_user,posts=posts,top_5=top_5)
