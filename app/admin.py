
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField

from .models import SiteInfo, Product, Category
from . import app, db, admin


def create_image_field(label, description=''):
    return ImageUploadField(
        label,
        base_path=app.config['UPLOAD_BASE_PATH'],     # куда сохранять на диске
        url_relative_path=app.config['UPLOAD_URL_PREFIX'],  # что подставлять в src
        #max_size=(1200, 1200, True),
        description=description
    )


class SiteInfoAdmin(ModelView):
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


class ProductAdmin(ModelView):
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


class CategoryAdmin(ModelView):
    column_list = ['name']
    form_excluded_columns = ('products',)  # Скрыть обратную связь
    column_labels = {'name': 'Название категории'}


def init_admin():
    """Регистрация всех моделей в админке."""
    admin.add_view(SiteInfoAdmin(SiteInfo, db.session, name='Страница'))
    admin.add_view(ProductAdmin(Product, db.session, name='Продукты'))
    admin.add_view(CategoryAdmin(Category, db.session, name='Категории'))
