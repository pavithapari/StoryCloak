from flask import Blueprint
from flask import render_template, request,flash,redirect,url_for
from app.users.forms import LoginForm,SignupForm,UserForm,RequestResetForm,ResetPasswordForm
from flask_login import current_user, login_user, logout_user,login_required
from datetime import datetime
from app.utils import save_avatar,save_picture,delete_old_avatar,send_reset_email,send_confirmation_email,send_welcome
from app.models import Post

users = Blueprint('users', __name__)
from app import db, bcrypt
from app.models import User

@users.route('/login',methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
                if not user.is_confirmed:
                    flash('Please confirm your email before logging in.', 'warning')
                    return redirect(url_for('users.login'))
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
            user=User.query.filter_by(email=form.email.data).first()
            send_confirmation_email(user)
            flash("Your account has been created successfully! Please confirm your email before logging in.", "success")
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
            # Check if the email or username has changed and if they are unique
            if form.email.data != user.email:
                existing_user = User.query.filter_by(email=form.email.data).first()
                if existing_user:
                    flash("This email is already registered. Please use a different email.", "danger")
                    return redirect(url_for('users.profile'))
            if form.username.data != user.username:
                existing_user = User.query.filter_by(username=form.username.data).first()
                if existing_user:
                    flash("This username is already taken. Please choose a different username.", "danger")
                    return redirect(url_for('users.profile'))
            if form.username.data!= user.username or form.email.data != user.email:
                user.username = form.username.data
                user.email = form.email.data
                user.is_confirmed = False  # Reset confirmation status
                send_confirmation_email(user)  # Send confirmation email again
                flash("Your profile has been updated. Please confirm your new email.", "success")
                db.session.commit() 
            
            return redirect(url_for('users.login'))

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
    new_picture = save_avatar(current_user.email,suppress_errors=True)
    if new_picture is None:
        flash("Failed to reset profile picture. Please try again.", "danger")
        return redirect(url_for('users.profile'))
    else:
        delete_old_avatar(old_picture_path)
        current_user.profile_picture = new_picture
        db.session.commit()
        flash("Your profile picture has been reset successfully!", "success")
        return redirect(url_for('users.profile'))

@users.route("/reset_password",methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form= RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if not user:
            flash("This account is not registered!","danger")
        send_reset_email(user)
        flash("An email is send with instructions so you can reset it","info")

    return render_template("reset_request.html",form=form,now=datetime.now(),user=current_user)

@users.route("/reset_password/<token>",methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user=User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('users.reset_request'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_password
        db.session.commit()
        flash(f"Your password has been updated! Now you can log in!" ,"success")
        return redirect(url_for("users.login"))
    return render_template('reset_token.html',form=form,now=datetime.now(),user=current_user)

@users.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = current_user
    old_picture_path = user.profile_picture
    Post.query.filter_by(user_id=user.id).delete()

    # Delete the user from the database
    db.session.delete(user)
    db.session.commit()
    flash("Your account has been deleted successfully.", "success")
    if old_picture_path !='/avatars/test.svg':
        delete_old_avatar(old_picture_path)

    # Log out the user
    logout_user()

    return redirect(url_for('main.home'))

@users.route('/confirm/<token>')
def confirm_mail(token):
    user = User.verify_confirm_token(token)
    if not user:
        flash('Invalid or expired token', 'danger')
        return redirect(url_for('main.home'))

    if user.is_confirmed:
        flash('Account already confirmed. Please log in.', 'info')
    else:
        user.is_confirmed = True
        db.session.commit()
        send_welcome(user.email,user.username)
        flash('Your account has been confirmed!', 'success')

    return redirect(url_for('users.login'))

