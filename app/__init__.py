# app/__init__.py
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import Babel
from config import Config

# Расширения создаём глобально, но инициализируем через init_app()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'login'
babel = Babel()


def create_app():
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

    from .views import bp as main_bp
    app.register_blueprint(main_bp)

    # Импортируем здесь, чтобы избежать circular import
    from .admin import init_admin
    from . import views, models

    # Подключаем админку с кастомным индексом

    init_admin(app)  # регистрируем модели в админке

    # Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    # Создаём заглушку SiteInfo, если нет ни одной записи
    """with app.app_context():
        if models.SiteInfo.query.count() == 0:
            db.session.add(
                models.SiteInfo(
                    company_name='Название компании',
                    main_page_text='Добро пожаловать на сайт',
                    email='info@example.com',
                    main_image='images/main.jpg'  # путь к заглушке
                )
            )
            db.session.commit()"""

    return app
