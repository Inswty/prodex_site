import logging
from http import HTTPStatus

from flask import (
    abort, Blueprint, current_app, flash, redirect, render_template, request,
    send_from_directory, url_for
)
from flask_login import login_user, logout_user
from werkzeug.exceptions import NotFound

from .email_service import send_feedback_email
from .exceptions import ProductNotFound
from .forms import ContactForm
from .models import Category, Product, SiteInfo, User

bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)


@bp.route('/login', methods=('GET', 'POST'))
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
            logger.warning('Неудачная попытка входа. Username=%s, IP=%s',
                           username, request.remote_addr)
            flash('Неверный логин или пароль', 'error')
    return render_template('admin/login.html')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@bp.route('/')
def index():
    try:
        return render_template('index.html', site=SiteInfo.get())
    except Exception as e:
        logger.error('Ошибка загрузки страницы /index: %s', e)
        abort(HTTPStatus.INTERNAL_SERVER_ERROR)


@bp.route('/products')
def products():
    try:
        return render_template(
            'products.html',
            site=SiteInfo.get(),
            categories=Category.get()
        )
    except Exception as e:
        logger.error('Ошибка загрузки страницы /products: %s', e)
        abort(HTTPStatus.INTERNAL_SERVER_ERROR)


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
    try:
        return render_template('about.html', site=SiteInfo.get())
    except Exception as e:
        logger.error('Ошибка загрузки страницы /about: %s', e)
        abort(HTTPStatus.INTERNAL_SERVER_ERROR)


@bp.route('/contacts', methods=('GET', 'POST'))
def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        # Отправка письма
        try:
            send_feedback_email(form)
            flash('Ваше сообщение отправлено!', 'success')
            return redirect(url_for('main.contacts'))
        except Exception:
            flash('Не удалось отправить сообщение. Попробуйте позже.', 'error')

    # GET-запрос или ошибка валидации
    return render_template(
        'contacts.html',
        site=SiteInfo.get(),
        form=form
    )


@bp.route('/media/<path:filename>')
def media(filename):
    try:
        return send_from_directory(
            current_app.config['UPLOAD_BASE_PATH'], filename
        )
    except NotFound:
        logger.warning('Файл не найден в /media: %s', filename)
        abort(HTTPStatus.NOT_FOUND)
