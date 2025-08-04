from flask import Blueprint,render_template
import requests

from flask_login import current_user
from datetime import datetime
errors=Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html',now=datetime,user=current_user), 404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html',now=datetime,user=current_user), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html',now=datetime,user=current_user), 500

@errors.app_errorhandler(requests.exceptions.ConnectionError)
def handle_connection_error(e):
    return render_template('errors/connection_error.html', now=datetime.now(), user=current_user), 503
