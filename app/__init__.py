from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask_jsonrpc import JSONRPC
import logging

from config import ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, API_URL, basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail(app)

jsonrpc = JSONRPC(app, API_URL, enable_web_browsable_api=True)

if not app.debug and MAIL_SERVER != '':
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'flapi fail', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
    appLogging = app.logger

if not app.debug:
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(basedir + '/tmp/flapi.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.DEBUG)
    app.logger.info('FLAPI startup')
    appLogging = app.logger

from app import views
from app.models import *
from app.api import *
