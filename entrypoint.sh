#!/bin/sh

set -e  # прерываем скрипт при любой ошибке

echo "Applying migrations..."
flask db upgrade

echo "Adding default SiteInfo if not exists..."
python << EOF
from app import create_app, db
from app.models import SiteInfo, User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    if not SiteInfo.query.first():
        db.session.add(
            SiteInfo(
                company_name='Название компании',
                main_page_text='Добро пожаловать на сайт',
                email='info@example.com',
                main_image='main.jpg'  # путь к заглушке
            )
        )
        db.session.commit()
        print("Default SiteInfo added")
    else:
        print("SiteInfo already exists")
    # Создаем админ-пользователя
    admin_username = "admin"
    admin_password = "secret123"
    if not User.query.first():
        db.session.add(
            User(
                username=admin_username,
                password_hash=generate_password_hash(admin_password),
                is_admin=True
            )
        )
        db.session.commit()
        print(f"Default admin user '{admin_username}' created with password '{admin_password}', Please change password!!!")
EOF

echo "Starting Gunicorn..."
if [ "$FLASK_ENV" = "development" ] || [ "$FLASK_DEBUG" = "1" ]; then
    exec gunicorn --workers 1 --reload --bind 0.0.0.0:5000 "app:create_app()"
else
    exec gunicorn --workers 1 --bind 0.0.0.0:5000 "app:create_app()"
fi
