from flask import Blueprint
from flask import render_template, request,flash,redirect,url_for
from app.users.forms import LoginForm,SignupForm,UserForm
from flask_login import current_user, login_user, logout_user,login_required
from datetime import datetime
from app.utils import save_avatar,save_picture,delete_old_avatar
users = Blueprint('users', __name__)
from app import db, bcrypt
from app.models import User

@users.route('/login',methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user, remember=form.remember.data) 
                flash("Login successful!", "success")
                next_page = request.args.get('next') # i use get() for error handling
                if next_page:
                    return redirect(next_page)
                return redirect(url_for("main.home"))
        else:
                flash("Login failed. Please check your email and password.", "danger")
    return render_template("login.html",now=datetime.now(), year=datetime.now().year, form=form,user=current_user)
@users.route('/signup',methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            picture = save_avatar(form.email.data)  # FIXED HERE

            user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password,
                profile_picture=picture
            )
            db.session.add(user)
            db.session.commit()
            flash("Your account has been created successfully! You can now log in.", "success")
            return redirect(url_for('users.login'))
    return render_template("signup.html", now=datetime.now(), year=datetime.now().year, form=form, user=current_user)


@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form=UserForm()
    user = current_user
    if request.method =='GET':
         form.username.data=user.username
         form.email.data=user.email
    if request.method == 'POST':
        if form.validate_on_submit():
            user.username = form.username.data
            user.email = form.email.data
            db.session.commit() 
            flash("Your profile has been updated successfully!", "success")
            return redirect(url_for('users.profile'))

    return render_template("profile.html",now=datetime.now(),year=datetime.now().year,form=form,user=user,posts=user.posts)

@users.route('/logout')
def logout():
     logout_user()
     return redirect(url_for('main.home'))

@users.route('/upload_profile_picture', methods=['POST'])
@login_required
def upload_profile_picture():
    form=UserForm()
    if 'profile_picture' not in request.files:
        flash("No file part in the request", "danger")
        return redirect(url_for('users.profile'))
    picture=form.profile_picture.data
    if picture:
        old_picture_path = current_user.profile_picture
        newpath = save_picture(picture, current_user.email)
        if newpath is None:
            flash("Failed to save new picture. Please try again.", "danger")
            return redirect(url_for('users.profile'))
        else:
            delete_old_avatar(old_picture_path)  # Delete old avatar if it exists
            current_user.profile_picture = newpath
            db.session.commit()
            flash("Your profile picture has been updated successfully!", "success")
            return redirect(url_for('users.profile'))
    else:
        flash("No picture uploaded", "danger")
        return redirect(url_for('users.profile'))
@users.route('/profile/reset_picture', methods=['POST'])
@login_required
def reset_profile_picture():
    old_picture_path = current_user.profile_picture
    new_picture = save_avatar(current_user.email)
    if new_picture is None:
        flash("Failed to reset profile picture. Please try again.", "danger")
        return redirect(url_for('users.profile'))
    else:
        delete_old_avatar(old_picture_path)
        current_user.profile_picture = new_picture
        db.session.commit()
        flash("Your profile picture has been reset successfully!", "success")
        return redirect(url_for('users.profile', toast='reset-success'))

