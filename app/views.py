from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from .models import SiteInfo, Category, Product, User

bp = Blueprint('main', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.index'))
        else:
            flash('Неверный логин или пароль', 'error')
    return render_template('login.html')


@bp.route('/logout')
def logout():
    logout_user()  # завершает сессию текущего пользователя
    return redirect(url_for('main.login'))  # редирект на страницу входа


@bp.route('/')
def index():
    site = SiteInfo.query.first()
    return render_template('index.html', site=site)


@bp.route('/products')
def products():
    site = SiteInfo.query.first()
    categories = Category.query.all()
    return render_template('products.html', site=site, categories=categories)


@bp.route('/product/<int:product_id>')
def product_detail(product_id):
    site = SiteInfo.query.first()
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', site=site, product=product)


@bp.route('/about')
def about():
    site = SiteInfo.query.first()
    return render_template('about.html', site=site)


@bp.route('/contacts')
def contacts():
    site = SiteInfo.query.first()
    return render_template('contacts.html', site=site)
