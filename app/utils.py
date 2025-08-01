import os
import secrets
from PIL import Image
from werkzeug.utils import secure_filename
from flask import current_app,flash,url_for
from flask_login import current_user
import requests
from app import mail
from flask_mail import Message

def save_avatar(email):
    url = f"https://api.dicebear.com/9.x/fun-emoji/svg?seed={email}&mouth=cute,kissHeart,lilSmile,plain,shy,smileLol,smileTeeth,tongueOut,wideSmile"
    response = requests.get(url)

    if response.status_code == 200:
        base_path = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(base_path, "static", "avatars")
        os.makedirs(folder_path, exist_ok=True)
        print(response.status_code)
        random_hex = secrets.token_hex(4) 
        filename = f"{random_hex}_{secure_filename(email)}.svg"
        file_path = os.path.join(folder_path, filename)

        with open(file_path, "wb") as f:
            f.write(response.content)
            flash("Avatar saved successfully!", "success")

        return f"/avatars/{filename}"  # Relative path for HTML use
    else:
        flash("Failed to save avatar. Using default avatar.", "error")
        return "/avatars/test.svg"  # Fallback avatar

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
            <div style="max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 10px;">
            <h2 style="color: #333;">Hi {user.username},</h2>
            <p>We received a request to reset your password. Click the button below to proceed:</p>
            <a href="{url_for('users.reset_token', token=token, _external=True)}"
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

