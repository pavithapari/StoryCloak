from flask import Blueprint,render_template, request,flash,url_for,redirect
from datetime import datetime
from app import db
from flask_login import current_user,login_required
from app.posts.forms import PostForm
posts = Blueprint('posts', __name__)
from app.models import Post,User

@posts.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        selected_tags = request.form.getlist('tags')  # gets checkbox values from HTML
        tags_string = ','.join(selected_tags) if selected_tags else None

        post = Post(
            title=form.title.data,
            content=form.content.data,
            tags=tags_string,
            visibility=form.visibility.data,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash("Your post is uploaded successfully!", "success")
        return redirect(url_for('main.home'))

    return render_template('create_post.html', form=form, now=datetime.now(), year=datetime.now().year, user=current_user)

@posts.route('/latest_posts')
def latest_posts():
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template('latest_posts.html', posts=posts, now=datetime.now(), year=datetime.now().year, user=current_user)


@posts.route('/<username>/all_posts')
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_posts.html', user=user, posts=user.posts,now=datetime.now())

@posts.route('/details/delete',methods=['POST'])
@login_required
def delete_post():
    Post.query.delete()
    User.query.delete()
    flash("All posts and users have been deleted successfully!", "success")
    db.session.commit()
    return redirect(url_for('main.home'))




