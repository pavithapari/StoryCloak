from flask import Blueprint,render_template
import requests
from flask import Blueprint, render_template,current_app
from sqlalchemy.exc import SQLAlchemyError
from flask_login import current_user
from datetime import datetime
from werkzeug.exceptions import BadRequest
from requests.exceptions import RequestException
errors=Blueprint('errors', __name__)

@errors.app_errorhandler(SQLAlchemyError)
def handle_sqlalchemy_error(error):
    current_app.logger.error(f"[SQLAlchemy Error] {str(error)}")
    return render_template("errors/database_error.html"), 500


@errors.app_errorhandler(404)
def error_404(error):
    current_app.logger.error(f"[404 Error] {str(error)}")
    return render_template('errors/404.html',now=datetime,user=current_user), 404

@errors.app_errorhandler(403)
def error_403(error):
    current_app.logger.error(f"[403 Error] {str(error)}")
    return render_template('errors/403.html',now=datetime,user=current_user), 403

@errors.app_errorhandler(500)
def error_500(error):
    current_app.logger.error(f"[500 Error] {str(error)}")
    return render_template('errors/500.html',now=datetime,user=current_user), 500

@errors.app_errorhandler(requests.exceptions.ConnectionError)
def handle_connection_error(e):
    current_app.logger.error(f"[Connection Error] {str(e)}")
    return render_template('errors/connection_error.html', now=datetime.now(), user=current_user), 503

@errors.app_errorhandler(requests.exceptions.Timeout)
def handle_timeout_error(e):
    current_app.logger.error(f"[Timeout Error] {str(e)}")
    return render_template('errors/timeout_error.html', now=datetime.now(), user=current_user), 504


@errors.app_errorhandler(BadRequest)
def handle_bad_request(error):
    current_app.logger.warning(f"[Bad Request] {str(error)}")
    return render_template("errors/400.html", now=datetime.now(), user=current_user), 400

@errors.app_errorhandler(Exception)
def handle_generic_error(e):

    current_app.logger.error(f"[Generic Error] {str(e)}")
    return render_template('errors/generic_error.html', now=datetime.now(), user=current_user), 500


