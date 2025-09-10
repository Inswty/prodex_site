import logging
from http import HTTPStatus

from flask import Blueprint, render_template, request

from . import db

bp = Blueprint('errors', __name__)
logger = logging.getLogger(__name__)


@bp.app_errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    logger.warning('404 ошибка: %s', request.url)
    return render_template('errors/404.html'), HTTPStatus.NOT_FOUND


@bp.app_errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    db.session.rollback()
    logger.error('500 ошибка: %s', error, exc_info=True)
    return render_template('errors/500.html'), HTTPStatus.INTERNAL_SERVER_ERROR
