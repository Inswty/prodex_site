from flask_admin import Admin
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel

from settings import Config

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)

# Настройка Babelex
app.config['BABEL_DEFAULT_LOCALE'] = 'ru'
app.config['BABEL_SUPPORTED_LOCALES'] = ['ru', 'en']
babel = Babel(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

admin = Admin(name='TNGT-Admin', template_mode='bootstrap4')
admin.init_app(app)

from . import views, models
from .admin import init_admin
init_admin()

with app.app_context():
    if models.SiteInfo.query.count() == 0:
        db.session.add(
            models.SiteInfo(
                company_name='Название компании',
                main_page_text='Добро пожаловать на сайт',
                email='info@example.com',
                main_image='images/main.jpg'  # путь к заглушке
            )
        )
        db.session.commit()