#!/bin/sh

set -e  # прерываем скрипт при любой ошибке

echo "Applying migrations..."
flask db upgrade

echo "Adding default SiteInfo if not exists..."
python << EOF
from app import create_app, db
from app.models import SiteInfo, User
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    if not SiteInfo.query.first():
        try:
            db.session.add(
                SiteInfo(
                    company_name='Название компании',
                    main_page_text='Добро пожаловать на сайт',
                    email='info@example.com',
                    main_image='main.jpg'  # путь к заглушке
                )
            )
            db.session.commit()
            app.logger.info('SiteInfo - Добавлена Default запись')
        except SQLAlchemyError  as e:
            app.logger.critical(f'SQLAlchemyError при попытке записи: {e}')
    # Создаем админ-пользователя
    admin_username = "admin"
    admin_password = "secret123"
    if not User.query.first():
        try:
            db.session.add(
                User(
                    username=admin_username,
                    password_hash=generate_password_hash(admin_password),
                    is_admin=True
                )
            )
            db.session.commit()        
            app.logger.info(f'Создан admin-пользователь: "{admin_username}", пароль: "{admin_password}". Измените пароль!!!')
        except SQLAlchemyError  as e:
            app.logger.critical(f'SQLAlchemyError при попытке создания пользователя: {e}')
EOF
# Копируем default main_image в /media
if [ ! -f /app/media/main.jpg ]; then
    cp /app/app/static/media/main.jpg /app/media/main.jpg
    echo "Файл main.jpg скопирован в /media"
else
    echo "Файл main.jpg уже существует в /media"
fi
echo "Starting Gunicorn..."
if [ "$FLASK_ENV" = "development" ] || [ "$FLASK_DEBUG" = "1" ]; then
    exec gunicorn --workers 1 --reload --bind 0.0.0.0:5000 --log-level error "app:create_app()"
else
    exec gunicorn --workers 1 --bind 0.0.0.0:5000 --log-level error "app:create_app()"
fi
