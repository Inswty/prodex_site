import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    TIMEZONE = 'Europe/Moscow'

    UPLOAD_BASE_PATH = '/app/media'
    UPLOAD_URL_PREFIX = '/media/'

    if os.getenv('FLASK_ENV') == 'production':
        SERVER_NAME = os.getenv('SERVER_NAME')
