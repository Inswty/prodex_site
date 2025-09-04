from http import HTTPStatus

from flask import (
    abort, Blueprint, flash, redirect, render_template, request, url_for
)
from flask_login import login_user, logout_user

from .exceptions import ProductNotFound
from .models import Category, Product, SiteInfo, User

bp = Blueprint('main', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get(username=username)
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.index'))
        else:
            flash('Неверный логин или пароль', 'error')
    return render_template('login.html')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@bp.route('/')
def index():
    return render_template('index.html', site=SiteInfo.get())


@bp.route('/products')
def products():
    return render_template(
        'products.html',
        site=SiteInfo.get(),
        categories=Category.get()
    )


@bp.route('/product/<int:product_id>')
def product_detail(product_id):
    try:
        product = Product.get_by_id(product_id)
    except ProductNotFound:
        abort(HTTPStatus.NOT_FOUND)

    return render_template(
        'product_detail.html',
        site=SiteInfo.get(),
        product=product
    )


@bp.route('/about')
def about():
    return render_template('about.html', site=SiteInfo.get())


@bp.route('/contacts')
def contacts():
    return render_template('contacts.html', site=SiteInfo.get())
