# -*- coding: utf8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# email server
MAIL_SERVER = ''  # your mailserver
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# administrator list
ADMINS = ['admin@site.ru']

# mongodb config
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017

# server config
PRODUCTION = False
APP_HOST = '0.0.0.0'
APP_PORT = 8888
API_URL = '/api'
