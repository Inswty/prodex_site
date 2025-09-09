import logging

from flask import Flask
from flask_babel import Babel
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
babel = Babel()


def create_app():
    """Создает и настраивает экземпляр Flask-приложения."""

    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)

    # Настройки Babel
    app.config['BABEL_DEFAULT_LOCALE'] = 'ru'
    app.config['BABEL_SUPPORTED_LOCALES'] = ['ru', 'en']

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    babel.init_app(app)

    # Blueprint для ошибок
    from .errors_handlers import bp as errors_bp
    app.register_blueprint(errors_bp)

    # Основной blueprint
    from .views import bp as main_bp
    app.register_blueprint(main_bp)

    from .sitemap import bp as sitemap_bp
    app.register_blueprint(sitemap_bp)

    # Импорт моделей и админки
    from . import models
    from .admin import init_admin
    from .logging_handler import DBHandler

    init_admin(app)

    # Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    # Настройка логирования
    handler = DBHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s, %(levelname)s, %(message)s, %(name)s'
    )
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    return app
