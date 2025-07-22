from flask import Blueprint,render_template, request,flash
from datetime import datetime
from app import db
from app.posts.forms import PostForm
posts = Blueprint('posts', __name__)
from app.models import Post

@posts.route('/create_post',methods=['GET', 'POST'])
def create_post():
    form=PostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            post = Post(
                title=form.title.data,
                content=form.content.data,
                tags=form.tags.data,
                visibility=form.visibility.data,
                author='current_user',  # Replace with actual user logic
            )
            db.session.add(post)
            db.session.commit()
            flash("Your post is uploaded successfully!", "success")
            
    return render_template('create_post.html', form=form, now=datetime.now(), year=datetime.now().year)

