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

    # Настройки почты
    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 587     # 465 (SSL)
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # твой email
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # пароль приложения Gmail
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')
