import os
basedir = os.path.abspath(os.path.dirname(__file__))
POST_PER_PAGE = 5
PRODUCT_PER_PAGE = 10
SERVICE_PER_PAGE = 10
SITE_WIDTH = 800

APP_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, 'data.db')
DEBUG = False
SECRET_KEY = os.urandom(24) # Used by Flask to encrypt session cookie.
POST_PER_PAGE = 5
MAIL_HOTNAME = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USEENAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
