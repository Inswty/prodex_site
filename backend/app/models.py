from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .constants import (
    MAX_STR_LENGHT, MAX_IMAGE_LENGTH, MAX_COMPONY_NAME_LENGTH,
    MAX_EMAIL_LENGTH, MAX_PHONE_LENGTH, MAX_ADRESS_LENGTH,
    MAX_CATEGORY_NAME_LENGTH, MAX_PRODUCT_NAME_LENGTH,
    MAX_USERNAME_LENGTH, MAX_PASSWORD_HASH_LENGTH, MAX_LEVEL_LOG_LENGTH
)
from .exceptions import ProductNotFound


class SiteInfo(db.Model):
    """Модель для хранения информации о компании."""

    id = db.Column(db.Integer, primary_key=True)
    main_page_text = db.Column(db.Text, nullable=False)
    main_image = db.Column(db.String(MAX_IMAGE_LENGTH), nullable=False)
    company_name = db.Column(
        db.String(MAX_COMPONY_NAME_LENGTH), nullable=False
    )
    about = db.Column(db.Text)
    email = db.Column(db.String(MAX_EMAIL_LENGTH), nullable=False)
    phone = db.Column(db.String(MAX_PHONE_LENGTH),)
    address = db.Column(db.String(MAX_ADRESS_LENGTH))

    @staticmethod
    def get():
        return SiteInfo.query.first()

    def __str__(self):
        return self.company_name[:MAX_STR_LENGHT]


class Category(db.Model):
    """Модель для категорий продуктов."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_CATEGORY_NAME_LENGTH), nullable=False)

    @staticmethod
    def get():
        return Category.query.all()

    def __str__(self):
        return self.name[:MAX_STR_LENGHT]


class Product(db.Model):
    """Модель для продуктов."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_PRODUCT_NAME_LENGTH), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.Text, nullable=False)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('category.id'),
        nullable=False
    )
    category = db.relationship('Category', backref='products', lazy=True)

    thumbnail = db.Column(db.String(MAX_IMAGE_LENGTH))
    header_image = db.Column(db.String(MAX_IMAGE_LENGTH))
    content_image = db.Column(db.String(MAX_IMAGE_LENGTH))

    @staticmethod
    def get_by_id(product_id):
        product = Product.query.get_or_404(product_id)
        if product is None:
            raise ProductNotFound(f'Продукт {product_id} не найден')
        return product

    def __str__(self):
        return self.name[:MAX_STR_LENGHT]


class User(UserMixin, db.Model):
    """Модель пользователя с поддержкой аутентификации через Flask-Login."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(MAX_USERNAME_LENGTH), unique=True, nullable=False
    )
    password_hash = db.Column(
        db.String(MAX_PASSWORD_HASH_LENGTH), nullable=False
    )
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get(username):
        return User.query.filter_by(username=username).first()

    def __str__(self):
        return self.username[:MAX_STR_LENGHT]


class Log(db.Model):
    """Модель для логирования событий."""

    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(MAX_LEVEL_LOG_LENGTH), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.now(timezone.utc)
    )
    logger_name = db.Column(db.String(100))

    @property
    def local_created_at(self):
        """Возвращает время в локальном часовом поясе."""
        if self.created_at:
            if self.created_at.tzinfo is None:
                utc_time = self.created_at.replace(tzinfo=timezone.utc)
            else:
                utc_time = self.created_at
            return utc_time.astimezone()
        return self.created_at
