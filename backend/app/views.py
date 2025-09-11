import os
from http import HTTPStatus

from flask import (
    abort, Blueprint, current_app, flash, redirect, render_template, request,
    send_from_directory, url_for
)
from flask_login import login_user, logout_user
from flask_mail import Mail, Message

from .exceptions import ProductNotFound
from .forms import ContactForm
from .models import Category, Product, SiteInfo, User

bp = Blueprint('main', __name__)


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
            flash('Неверный логин или пароль', 'error')
    return render_template('admin/login.html')


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


@bp.route('/contacts', methods=('GET', 'POST'))
def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        # Отправка письма
        mail = Mail(current_app)
        msg = Message(
            subject=(
                f'Сообщение с сайта Prodex_site от пользователя: '
                f'{form.name.data}'
            ),
            recipients=[os.getenv('MAIL_USERNAME')],  # сюда приходят письма
            body=(
                f'Имя: {form.name.data}\n'
                f'Email: {form.email.data}\nТелефон: {form.phone.data}\n\n'
                f'Сообщение:\n{form.message.data}'
            )
        )
        mail.send(msg)
        flash('Ваше сообщение отправлено! Спасибо 🙏', 'success')
        return redirect(url_for('main.contacts'))  # перезагрузка страницы

    # GET-запрос или ошибка валидации
    return render_template(
        'contacts.html',
        site=SiteInfo.get(),
        form=form  # передаём форму в шаблон
    )


@bp.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(
        current_app.config['UPLOAD_BASE_PATH'], filename
    )
