import os
import secrets
from PIL import Image
from werkzeug.utils import secure_filename
from flask import current_app,flash,url_for
from flask_login import current_user
import requests
from app import mail
from flask_mail import Message
from requests.exceptions import RequestException


def save_avatar(email, suppress_errors=True):
    try:
        url = f"https://api.dicebear.com/9.x/fun-emoji/svg?seed={email}&mouth=cute,kissHeart,lilSmile,plain,shy,smileLol,smileTeeth,tongueOut,wideSmile"
        response = requests.get(url)
        response.raise_for_status()
        return url

    except RequestException as e:
        if suppress_errors:
            return "https://api.dicebear.com/9.x/fun-emoji/svg?seed=Eliza"
        else:
            # Let the error bubble up to trigger Flask's app_errorhandler
            raise





def send_reset_email(user):
    token= user.get_reset_token()
    msg=Message(subject='Password Reset Request', sender=('StoryCloak','pavithapariofficial@gmail.com'),
                recipients=[user.email])
    msg.html = f"""
<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
    <div style="max-width: 600px; margin: auto; background: antiquewhite; padding: 30px; border-radius: 10px; text-align: center;">
        
        <!-- Logo Image -->
        <img src="https://i.postimg.cc/z3XVNHQr/logo.png" alt="StoryCloak Logo" style="width: 120px; margin-bottom: 20px;">

        <h2 style="color: #333;">Hi {{ user.username }},</h2>
        <p>We received a request to reset your password. Click the button below to proceed:</p>
        
        <a href="{{ url_for('users.reset_token', token=token, _external=True) }}"
            style="display: inline-block; padding: 10px 20px; background-color: #007BFF; color: white;
                    text-decoration: none; border-radius: 5px; font-weight: bold;">
            Reset Password
        </a>
        
        <p style="margin-top: 20px;">If you didn’t make this request, feel free to ignore this email.</p>
        <p style="color: #888;">— StoryCloak Team</p>
    </div>
</body>
</html>
    """

    mail.send(msg)


def send_confirmation_email(user):
    token = user.get_confirm_token()
    msg = Message(subject="Confirm Your Email",
                  sender=("StoryCloak", "pavithapariofficial@gmail.com"),
                  recipients=[user.email])
    msg.html = f"""
<html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background: antiquewhite; padding: 30px; border-radius: 10px;">
            <!-- Logo -->
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="https://i.postimg.cc/z3XVNHQr/logo.png" alt="StoryCloak Logo" style="max-width: 150px;">
            </div>

            <h2 style="color: #333;">Hello {user.username},</h2>
            <p>Please confirm your email by clicking the button below:</p>
            <br>
            <a href="{url_for('users.confirm_mail', token=token, _external=True)}"
               style="padding:10px 20px; background-color:#007BFF; color:white; text-decoration:none; border-radius:5px;">
               Confirm Email
            </a>
            <br><br>
            <p>If you did not create/update an account, you can safely ignore this email.</p>
            <p>Thank you for joining StoryCloak!</p>
            <p style="color: #888;">— The StoryCloak Team</p>
        </div>
    </body>
</html>

    """
    mail.send(msg)

def send_welcome(email,name):
    msg = Message(subject="Welcome to StoryCloak",
                  sender=("StoryCloak", "pavithapariofficial@gmail.com"),
                  recipients=[email])
    msg.html = f"""
<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
    <div style="max-width: 600px; margin: auto; background: antiquewhite; padding: 30px; border-radius: 10px; text-align: center;">
        
        <!-- Logo at the top -->
        <img src="https://i.postimg.cc/z3XVNHQr/logo.png" alt="StoryCloak Logo" style="max-width: 150px; margin-bottom: 20px;">

        <h2 style="color: #333;">Welcome to StoryCloak, {name}!</h2>
        <p>We're absolutely delighted to welcome you to our StoryCloak family.</p>
        <p>Here, every story matters and every voice is cherished. We hope you find inspiration, friendship, and joy as you explore and share your own tales.</p>
        <p>Thank you for bringing your unique perspective to our community. If you ever need help or just want to say hello, we're always here for you.</p>
        <p style="margin-top: 20px;">Wishing you wonderful adventures ahead!</p>
        <p style="color: #888;">— With warmth, The StoryCloak Team</p>
    </div>
</body>
</html>
    """
    mail.send(msg)
    
