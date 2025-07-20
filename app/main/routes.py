from flask import Blueprint

from flask import render_template, request
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def home():
    current_year = datetime.now().year
    return render_template('home.html', now=datetime.now(), year=current_year)