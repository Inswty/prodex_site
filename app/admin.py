
from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField
from flask_login import current_user, logout_user
from flask_admin import Admin, AdminIndexView, expose
from wtforms import Form, StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length
from flask_admin.menu import MenuLink
from config import Config

from .models import SiteInfo, Product, Category, User
from . import db


class SecureModelView(ModelView):
    """Доступ только для авторизованных админов."""
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))  # если нет доступа


def create_image_field(label, description=''):
    return ImageUploadField(
        label,
        base_path=Config.UPLOAD_BASE_PATH,
        url_relative_path=Config.UPLOAD_URL_PREFIX,
        description=description
    )


class SiteInfoAdmin(SecureModelView):
    can_create = False  # отключает кнопку 'Create'
    can_delete = False  # отключает кнопку 'Delete'
    column_list = ['company_name', 'email', 'phone']
    # Русификация заголовков
    column_labels = {
        'company_name': 'Наименование',
        'main_page_text': 'Текст на главной',
        'main_image': 'Изображение шапки',
        'about': 'О компании',
        'email': 'email',
        'phone': 'Телефон',
        'address': 'Адрес'

    }
    form_widget_args = {
        'main_page_text': {
            'rows': 15,  # Высота в строках
        },
        'about': {
            'rows': 7,
        }
    }
    form_extra_fields = {
        'main_image': create_image_field('Основное изображение сайта')
    }


class ProductAdmin(SecureModelView):
    column_list = ['name', 'category', 'short_description']
    column_labels = {
        'name': 'Название',
        'description': 'Описание',
        'short_description': 'Краткое описание',
        'category': 'Категория',
        'thumbnail': 'Миниатюра',
        'header_image': 'Изображение шапки',
        'content_image': 'Изображение продукта'
    }
    form_columns = [
        'name', 'description', 'short_description', 'category',
        'thumbnail', 'header_image', 'content_image'
    ]
    form_ajax_refs = {
        'category': {
            'fields': ['name'],
            'page_size': 10,
            'minimum_input_length': 0  # Показывать все сразу
        }
    }
    form_widget_args = {
        'description': {
            'rows': 15,
        }
    }
    form_extra_fields = {
        'thumbnail': create_image_field(
            'Миниатюра для списка',
            'Небольшое изображение для списков и карточек товаров'
        ),
        'header_image': create_image_field(
            'Изображение в шапке',
            'Большое изображение для верхней части страницы товара'
        ),
        'content_image': create_image_field(
            'Изображение продукта',
            'Основное изображение в контенте страницы товара'
        )
    }


class CategoryAdmin(SecureModelView):
    column_list = ['name']
    form_excluded_columns = ['products']  # Скрыть обратную связь
    column_labels = {'name': 'Название категории'}


class UserAdmin(SecureModelView):
    class UserForm(Form):
        username = StringField('Username', validators=[DataRequired()])
        is_admin = BooleanField('Is Admin')
        new_password = PasswordField('Новый пароль', validators=[
            Length(min=6, message='Пароль должен быть не менее 6 символов')
        ])
    form = UserForm
    column_list = ['username', 'is_admin']

    def on_model_change(self, form, model, is_created):
        if form.new_password.data:
            model.set_password(form.new_password.data)


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for('main.login'))
        return super().index()

    @expose('/logout')
    def logout(self):
        logout_user()
        return redirect(url_for('main.login'))


admin = Admin(
    name='TNGT-Admin',
    template_mode='bootstrap4',
    index_view=MyAdminIndexView()
)


def init_admin(app):
    """Регистрация всех моделей в админке."""
    admin.init_app(app)
    admin.add_view(UserAdmin(User, db.session, name='Пользователи'))
    admin.add_view(SiteInfoAdmin(SiteInfo, db.session, name='Страница'))
    admin.add_view(ProductAdmin(Product, db.session, name='Продукты'))
    admin.add_view(CategoryAdmin(Category, db.session, name='Категории'))
    admin.add_link(MenuLink(name='Выйти', category='', url='/logout'))
