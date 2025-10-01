from flask import Blueprint,render_template, request,flash,url_for,redirect,jsonify
from datetime import datetime
from app import db
from flask_login import current_user,login_required
from app.posts.forms import PostForm
posts = Blueprint('posts', __name__)
from app.models import Post,User,Like,PrivateNote,SavePost
from sqlalchemy import func


@posts.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        selected_tags = request.form.getlist('tags')  # gets checkbox values from HTML
        tags_string = ','.join(selected_tags) if selected_tags else None
        if form.visibility.data == 'private':
            note = PrivateNote(
                title=form.title.data,
                content=form.content.data,
                visibility=form.visibility.data,
                author=current_user
            )
            db.session.add(note)
            db.session.commit()
            flash("Your note is saved successfully!", "success")
            return redirect(url_for('notes.show_notes'))
        if form.visibility.data == 'public':
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
    page=request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=4)
    return render_template('home.html', posts=posts, now=datetime.now(), year=datetime.now().year, user=current_user)


@posts.route('/<username>/all_posts')
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_posts.html', user=user, posts=user.posts,now=datetime.now())

@posts.route('/posts/<int:post_id>', methods=['POST','GET'])
def readmore(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('readmore.html', post=post, now=datetime.now(), year=datetime.now().year,user=current_user)

@posts.route('/posts/<int:post_id>/delete', methods=['POST','GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author == current_user:
        db.session.delete(post)
        db.session.commit()
        flash("Your post has been deleted successfully!", "success")
    else:
        flash("You do not have permission to delete this post.", "danger")
    return redirect(url_for('users.profile'))
@posts.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash("You do not have permission to edit this post.", "danger")
        return redirect(url_for('posts.user_posts', username=current_user.username))

    form = PostForm(obj=post)
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.visibility.data = post.visibility
        tags = post.tags.split(',') if post.tags else []

    if form.validate_on_submit():
        if form.visibility.data == 'private':
            note = PrivateNote(
                title=form.title.data,
                content=form.content.data,
                visibility=form.visibility.data,
                author=current_user
            )
            db.session.add(note)
            db.session.commit()
            db.session.delete(post)  # Delete the post after converting to note
            db.session.commit()
            flash("Your post has been changed into a note!", "success")
            return redirect(url_for('notes.show_notes'))
        
        if form.visibility.data == 'public':
            post.title = form.title.data
            post.content = form.content.data
            selected_tags = request.form.getlist('tags')  # gets checkbox values from HTML
            tags_string = ','.join(selected_tags) if selected_tags else None
            post.tags = tags_string
            if not post.tags:
                post.tags = None
            post.visibility = form.visibility.data
            db.session.commit()
            flash("Your post has been updated successfully!", "success")
            return redirect(url_for('posts.readmore', post_id=post.id))

    return render_template('create_post.html', form=form, post=post,user=current_user, now=datetime.now(),selected_tags=tags)

@posts.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    existing_like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()

    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
        return jsonify({'status': 'unliked', 'likes_count': len(post.likes)})
    else:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        return jsonify({'status': 'liked', 'likes_count': len(post.likes)})

@posts.route('/trending')
def trending():
    trending_posts = db.session.query(Post, func.count(Like.id).label('like_count'))\
        .outerjoin(Like, Post.id == Like.post_id)\
        .group_by(Post.id)\
        .order_by(func.count(Like.id).desc())\
        .limit(7).all()
    posts_only = [post for post, like_count in trending_posts]
    return render_template('home.html', posts=posts_only,user=current_user,now=datetime.now())

@posts.route('/humor')
def humor():
    page=request.args.get('page', 1, type=int)
    humor_posts = Post.query.filter(Post.tags.contains('humor')).order_by(Post.date_posted.desc()).paginate(page=page,per_page=4)
    return render_template('home.html', posts=humor_posts, user=current_user, now=datetime.now())

@posts.route('/tips')
def tips():
    page=request.args.get('page', 1, type=int)
    tech_posts = Post.query.filter(Post.tags.contains('tips')).order_by(Post.date_posted.desc()).paginate(page=page,per_page=4)
    return render_template('home.html', posts=tech_posts, user=current_user, now=datetime.now())
@posts.route('/reviews')
def reviews():
    page=request.args.get('page', 1, type=int)
    review_posts = Post.query.filter(Post.tags.contains('reviews')).order_by(Post.date_posted.desc()).paginate(page=page,per_page=4)
    return render_template('home.html', posts=review_posts, user=current_user, now=datetime.now())
@posts.route('/personal')
def personal():
    page=request.args.get('page', 1, type=int)
    personal_posts = Post.query.filter(Post.tags.contains('personal')).order_by(Post.date_posted.desc()).paginate(page=page,per_page=4)
    return render_template('home.html', posts=personal_posts, user=current_user, now=datetime.now())
@posts.route('/tech')
def tech():
    page=request.args.get('page', 1, type=int)
    tech = Post.query.filter(Post.tags.contains('tech')).order_by(Post.date_posted.desc()).paginate(page=page,per_page=4) 
    return render_template('home.html', posts=tech, user=current_user, now=datetime.now())

@posts.route('/none')
@login_required
def none():
    page=request.args.get('page', 1, type=int)
    none_posts = Post.query.filter(Post.tags.is_(None)).order_by(Post.date_posted.desc()).paginate(page=page,per_page=4) 
    return render_template('home.html', posts=none_posts, user=current_user, now=datetime.now())

@posts.route('/all')
@login_required
def all():
    page=request.args.get('page', 1, type=int)
    all_posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=4) 
    return render_template('home.html', posts=all_posts, user=current_user, now=datetime.now())

@posts.route('/save_posts/<int:post_id>', methods=['GET','POST'])
@login_required
def save_post(post_id):
    if request.method == 'POST':
        new=SavePost(user_id=current_user.id, post_id=post_id)
        db.session.add(new)
        db.session.commit()
        flash("Post saved successfully!", "success")
    return redirect(url_for('posts.saved_posts'))
@posts.route('/saved_posts', methods=['GET','POST'])
@login_required
def saved_posts():
    user=current_user
    saved_posts=Post.query.join(SavePost).filter(SavePost.user_id == user.id).order_by(Post.date_posted.desc()).all()
    if not saved_posts:
        flash("You have no saved posts.", "info")
        return redirect(url_for('posts.latest_posts'))
    return render_template('saved_posts.html', saved_posts=saved_posts, user=current_user, now=datetime.now())

@posts.route('/unsave_post/<int:post_id>', methods=['GET','POST'])
@login_required
def unsave_post(post_id):
    saved_post = SavePost.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if saved_post:
        db.session.delete(saved_post)
        db.session.commit()
        flash("Post unsaved successfully!", "success")
    return redirect(url_for('posts.saved_posts'))
