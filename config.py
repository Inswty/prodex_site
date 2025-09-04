import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    TIMEZONE = 'Europe/Moscow'

    # Путь до папки на диске (куда будут сохраняться файлы)
    UPLOAD_BASE_PATH = os.path.join(basedir, 'app', 'static', 'image')
    # URL-префикс для доступа к картинкам
    UPLOAD_URL_PREFIX = '/image/'
    if os.getenv('FLASK_ENV') == 'production':
        SERVER_NAME = 'tngt.duckdns.org'
