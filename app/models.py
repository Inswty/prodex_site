from . import db


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
