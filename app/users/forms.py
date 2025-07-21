from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired,Email,Length,EqualTo 

class LoginForm(FlaskForm):
    email=EmailField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')

class SignupForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=15)])
    email=EmailField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    con_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo(password)])
    
    submit=SubmitField('Sign Up')


