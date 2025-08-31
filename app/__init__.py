import logging

from flask import Flask
from flask_babel import Babel
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config


# Расширения создаём глобально, но инициализируем через init_app()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'login'
babel = Babel()


def create_app():
    """
    Создает и настраивает экземпляр Flask-приложения.

    Инициализирует расширения: SQLAlchemy, Migrate, Flask-Login и Babel,
    регистрирует blueprint для основных представлений.

    Возвращает:
        app (Flask): Экземпляр настроенного приложения Flask.
    """
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)

    # Настройки Babel
    app.config['BABEL_DEFAULT_LOCALE'] = 'ru'
    app.config['BABEL_SUPPORTED_LOCALES'] = ['ru', 'en']

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    babel.init_app(app)

    # Регистрация error blueprint
    from .errors_handlers import bp as errors_bp
    app.register_blueprint(errors_bp)

    # Регистрация основных blueprint'ов
    from .views import bp as main_bp
    app.register_blueprint(main_bp)

    # Импортируем здесь, чтобы избежать circular import
    from . import models
    from .admin import init_admin
    from .logging_handler import DBHandler

    init_admin(app)  # регистрируем модели в админке

    # Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        """
        Загружает пользователя по ID для Flask-Login.


        Возвращает:
            models.User: Пользователь, соответствующий данному ID, или None.
        """
        return models.User.query.get(int(user_id))

    handler = DBHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s, %(levelname)s, %(message)s, %(name)s'
    )
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    with app.app_context():
        app.logger.info(
            f'Приложение TNGT запущено, режим: '
            f'{"development" if app.debug else "production"}'
        )

    return app
