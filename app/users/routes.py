from flask import Blueprint
from flask import render_template, request,flash,redirect,url_for
from app.users.forms import LoginForm,SignupForm
from datetime import datetime
users = Blueprint('users', __name__)
from app import db, bcrypt
from app.models import User

@users.route('/login',methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
                flash("Login successful!", "success")
                return redirect(url_for("main.home"))
        else:
                flash("Login failed. Please check your email and password.", "danger")
    return render_template("login.html",now=datetime.now(), year=datetime.now().year, form=form)
@users.route('/signup',methods=['GET', 'POST'])
def signup():
    form=SignupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password,  
            )
            db.session.add(user)
            db.session.commit()
            flash("Your account has been created successfully! You can now log in.", "success")
            return redirect(url_for('users.login'))
    return render_template("signup.html", now=datetime.now(), year=datetime.now().year, form=form)



