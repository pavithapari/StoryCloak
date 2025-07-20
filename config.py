import os
class Config:
    SECRET_KEY = '3456kdngsokwejgi345'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_ID')
    MAIL_PASSWORD = os.environ.get('MAIL_PWD')