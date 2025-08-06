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

        base_path = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(base_path, "static", "avatars")
        os.makedirs(folder_path, exist_ok=True)

        random_hex = secrets.token_hex(4)
        filename = f"{random_hex}_{secure_filename(email)}.svg"
        file_path = os.path.join(folder_path, filename)

        with open(file_path, "wb") as f:
            f.write(response.content)
        return f"/avatars/{filename}"

    except RequestException as e:
        if suppress_errors:
            return "/avatars/test.svg"
        else:
            # Let the error bubble up to trigger Flask's app_errorhandler
            raise


def delete_old_avatar(old_picture_path):
    if not isinstance(old_picture_path, str):
        return current_user.profile_picture  # Ignore if it's not a string

    if "dicebear.com" in old_picture_path or "default" in old_picture_path:
        return  # Don't delete remote or default images

    # Remove leading slash, so it's a valid relative path inside /static/
    relative_path = old_picture_path.lstrip("/")
    full_path = os.path.join(current_app.root_path, 'static', relative_path)

    if os.path.exists(full_path):
        os.remove(full_path)
        print(f"Deleted old avatar at: {full_path}")

def save_picture(new_picture_file,email):
    # Save new image
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(new_picture_file.filename)
    if f_ext.lower() not in ['.jpg', '.jpeg', '.png']:
        flash("Invalid image format. Please upload a JPG, PNG, or GIF.", "error")
        return 
    picture_fn = secure_filename(email) + "_" + random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/avatars', picture_fn)
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)

    output_size = (300, 300)
    i = Image.open(new_picture_file)
    i.thumbnail(output_size)
    i.save(picture_path)
    flash("New image saved","success")
    return f"/avatars/{picture_fn}"



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
        <img src="{{ url_for('static', filename='logo.svg') }}" alt="StoryCloak Logo" style="width: 120px; margin-bottom: 20px;">

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
                <img src="{{ url_for('static', filename='logo.svg') }}" alt="StoryCloak Logo" style="max-width: 150px;">
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
        <img src="{{ url_for('static', filename='logo.svg') }}" alt="StoryCloak Logo" style="max-width: 150px; margin-bottom: 20px;">

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
    
