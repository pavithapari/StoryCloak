import os
import secrets
from PIL import Image
from werkzeug.utils import secure_filename
from flask import current_app,flash
import requests

def save_avatar(email):
    url = f"https://api.dicebear.com/9.x/fun-emoji/svg?seed={email}&mouth=cute,kissHeart,lilSmile,plain,shy,smileLol,smileTeeth,tongueOut,wideSmile"
    response = requests.get(url)

    if response.status_code == 200:
        base_path = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(base_path, "static", "avatars")
        os.makedirs(folder_path, exist_ok=True)
        print(response.status_code)
        filename = secure_filename(email) + ".svg"
        file_path = os.path.join(folder_path, filename)

        with open(file_path, "wb") as f:
            f.write(response.content)
            flash("Avatar saved successfully!", "success")

        return f"/avatars/{filename}"  # Relative path for HTML use
    else:
        flash("Failed to save avatar. Using default avatar.", "error")
        return "/avatars/test.webp"  # Fallback avatar

def delete_old_avatar(old_picture_path):
    if not isinstance(old_picture_path, str):
        return  # Ignore if it's not a string

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
    picture_fn = secure_filename(email) + "_" + random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/avatars', picture_fn)
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)

    output_size = (300, 300)
    i = Image.open(new_picture_file)
    i.thumbnail(output_size)
    i.save(picture_path)
    flash("New image saved","success")
    return f"/avatars/{picture_fn}"

