from flask import render_template
from .models import SiteInfo, Category, Product
from . import app


@app.route('/')
def index():
    site = SiteInfo.query.first()
    return render_template('index.html', site=site)


@app.route('/products')
def products():
    site = SiteInfo.query.first()
    categories = Category.query.all()
    return render_template('products.html', site=site, categories=categories)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    site = SiteInfo.query.first()
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', site=site, product=product)


@app.route('/about')
def about():
    site = SiteInfo.query.first()
    return render_template('about.html', site=site)


@app.route('/contacts')
def contacts():
    site = SiteInfo.query.first()
    return render_template('contacts.html', site=site)
