from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class SiteInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_page_text = db.Column(db.Text, nullable=False)
    main_image = db.Column(db.String(200), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    about = db.Column(db.Text)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50),)
    address = db.Column(db.String(200))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return self.name


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.Text, nullable=False)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('category.id'),
        nullable=False
    )
    category = db.relationship('Category', backref='products', lazy=True)

    thumbnail = db.Column(db.String(200))
    header_image = db.Column(db.String(200))
    content_image = db.Column(db.String(200))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
