from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired,Email,Length,EqualTo 
from wtforms import ValidationError
from app.models import User

class LoginForm(FlaskForm):
    email=EmailField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')

class SignupForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=15)])
    email=EmailField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    con_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    def validate_username(self, username):
        user=User.query.filter_by(username=username.data).first() # check if the username is already taken
        if user:
            raise ValidationError('This username is already taken please use different one')
    def validate_email(self, email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered please use different one')
    
    submit=SubmitField('Sign Up')


