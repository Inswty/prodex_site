import logging
import os
import uuid
from http import HTTPStatus

from flask import abort, flash, redirect, request, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField
from flask_admin.menu import MenuLink
from flask_login import current_user, logout_user
from sqlalchemy import delete
from wtforms import Form, StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length

from config import Config
from . import db
from .constants import (
    PAGINATION_PAGE_SIZE, MAIN_PAGE_TEXT_ROW_HEIGHT, ABOUT_ROW_HEIGHT,
    CATEGORY_AJAX_PAGE_SIZE, CATEGORY_AJAX_MIN_INPUT_LENGTH,
    PRODUCT_DESCRIPTION_ROW_HEIGHT
)
from .models import Category, Log, SiteInfo, Product, User

logger = logging.getLogger(__name__)


class AdminSecurityMixin:
    """Миксин для контроля доступа к админ-панели."""

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        logger.warning(
            'Попытка доступа к разделу "%s". Пользователь: %s',
            name,
            current_user
        )
        if not current_user.is_authenticated:
            return redirect(url_for('main.login'))
        return abort(HTTPStatus.FORBIDDEN)


class LogModelView (AdminSecurityMixin, ModelView):

    def after_model_change(self, form, model, is_created):
        """Логирование после изменения модели."""
        action = 'Создана' if is_created else 'Обновлена'
        logger.info(
            '%s запись в %s : %s',
            action,
            model.__class__.__name__,
            model
        )

    def after_model_delete(self, model):
        """Логирование после удаления модели."""
        logger.warning(
            'Запись %s удалена из: %s',
            model,
            model.__class__.__name__
        )


def create_image_field(label, description=''):
    """Создает поле загрузки изображения с уникальным именем файла."""

    def namegen(obj, file_data):
        # Получаем расширение исходного файла
        ext = os.path.splitext(file_data.filename)[1]
        # Генерируем уникальное имя через UUID
        return f'{uuid.uuid4().hex}{ext}'

    return ImageUploadField(
        label,
        base_path=Config.UPLOAD_BASE_PATH,
        endpoint='main.media',
        description=description,
        namegen=namegen
    )


class SiteInfoAdmin(LogModelView):
    """Админка для управления информацией о сайте."""

    can_create = False  # отключает кнопку 'Create'
    can_delete = False  # отключает кнопку 'Delete'
    column_list = ['company_name', 'email', 'phone']
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
            'rows': MAIN_PAGE_TEXT_ROW_HEIGHT,  # Высота в строках
        },
        'about': {
            'rows': ABOUT_ROW_HEIGHT,
        }
    }
    form_extra_fields = {
        'main_image': create_image_field('Основное изображение сайта')
    }


class ProductAdmin(LogModelView):
    """Админка для управления продуктами."""

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
            'page_size': CATEGORY_AJAX_PAGE_SIZE,
            'minimum_input_length': CATEGORY_AJAX_MIN_INPUT_LENGTH
        }
    }
    form_widget_args = {
        'description': {
            'rows': PRODUCT_DESCRIPTION_ROW_HEIGHT,
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


class CategoryAdmin(LogModelView):
    """Админка для управления категориями продуктов."""

    column_list = ['name']
    form_excluded_columns = ['products']  # Скрыть обратную связь
    column_labels = {'name': 'Название категории'}

    # запрет на удаление категорий с товарами
    def delete_model(self, model):
        if model.products:  # relationship с Product
            logger.warning(
                'Попытка удалить категорию с id=%s, в которой есть товары',
                model.name
            )
            flash('Нельзя удалить категорию, пока в ней есть товары', 'error')
            return False  # удаление не происходит
        return super().delete_model(model)


class UserAdmin(LogModelView):
    """Админка для управления пользователями."""

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


class LogsAdminIndexView(AdminSecurityMixin, AdminIndexView):
    """Главная страница админки с отображением логов."""

    @expose('/')
    def index(self):
        # Пагинация
        page = request.args.get('page', 1, type=int)
        per_page = PAGINATION_PAGE_SIZE

        # Получаем логи с пагинацией
        logs_pagination = Log.query.order_by(Log.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        logs = logs_pagination.items

        return self.render('admin/index.html',
                           logs=logs,
                           pagination=logs_pagination)

    @expose('/clear-logs', methods=['POST'])
    def clear_logs(self):
        """Очистка всех логов из БД."""
        try:
            # Удаляем все логи
            db.session.execute(delete(Log))
            db.session.commit()

            flash('Все логи успешно очищены', 'success')
            logger.info(
                'Логи удалены пользователем: %s',
                current_user.username
            )
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при очистке логов: {e}', 'error')
            logger.error('Ошибка очистки логов: %s', e)
        return redirect(url_for('admin.index'))

    @expose('/logout')
    def logout(self):
        logout_user()
        return redirect(url_for('main.login'))


# Создаем админку с кастомной главной страницей
admin = Admin(
    name='Prodex-Admin',
    template_mode='bootstrap4',
    index_view=LogsAdminIndexView(name='Logs')  # Переименовываем в 'Logs'
)


class LogEntryAdmin(LogModelView):
    """Админка для просмотра логов."""

    column_list = ('created_at', 'level', 'message', 'logger_name')
    column_filters = ('level', 'created_at')
    can_create = False
    can_edit = False
    can_delete = True
    column_searchable_list = ('message',)
    column_labels = {
        'created_at': 'Дата/Время',
        'level': 'Уровень',
        'message': 'Сообщение',
        'logger_name': 'Логгер'
    }


def init_admin(app):
    """Регистрация всех моделей в админке."""
    admin.init_app(app)
    admin.add_view(UserAdmin(User, db.session, name='Пользователи'))
    admin.add_view(SiteInfoAdmin(SiteInfo, db.session, name='Страница'))
    admin.add_view(ProductAdmin(Product, db.session, name='Продукты'))
    admin.add_view(CategoryAdmin(Category, db.session, name='Категории'))
    admin.add_link(MenuLink(name='Выйти', category='', url='/logout'))
