from flask import Blueprint
from flask import render_template, request
from app.users.forms import LoginForm,SignupForm
from datetime import datetime
users = Blueprint('users', __name__)

@users.route('/login')
def login():
    form=LoginForm()

    return render_template("login.html",now=datetime.now(), year=datetime.now().year, form=form)
@users.route('/signup')
def signup():
    form=SignupForm()


    return render_template("signup.html",now=datetime.now(), year=datetime.now().year, form=form)
