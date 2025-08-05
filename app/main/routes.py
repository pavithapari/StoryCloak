from flask import Blueprint

from flask import render_template, request
from flask_login import current_user
from datetime import datetime
from app.models import Post
from app.models import User,Like

main = Blueprint('main', __name__)

@main.route('/')
def home():
    current_year = datetime.now().year
    page=request.args.get('page', 1, type=int) # Get the page number from the query string, default to 1
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=4) 
    return render_template('home.html', now=datetime.now(), year=current_year,user=current_user,posts=posts)
@main.route('/details')
def details():
    likes=Like.query.all()
    users = User.query.all()
    return render_template('details.html', users=users,likes=likes)