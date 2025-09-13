import logging
import os

from flask import current_app
from flask_mail import Mail, Message

logger = logging.getLogger(__name__)


def send_feedback_email(form):
    """Отправляет сообщение с формы обратной связи на email."""

    try:
        mail = Mail(current_app)
        recipients = [os.getenv('MAIL_USERNAME')]  # сюда приходят письма
        body = (
            f'Имя: {form.name.data}\n'
            f'Email: {form.email.data}\nТелефон: {form.phone.data}\n\n'
            f'Сообщение:\n{form.message.data}'  # noqa: E231
        )
        msg = Message(
            subject=(
                f'Сообщение с сайта Prodex_site от пользователя: '
                f'{form.name.data}'
            ),
            recipients=recipients,
            body=body
        )
        mail.send(msg)
        logger.info(
            f'Сообщение от пользователя отправлено на {recipients}. '
            f'{body}'
        )
    except Exception as e:
        logger.error(
            f'Ошибка отправки сообщения с формы: {e}, Body: {body}',
            exc_info=True
        )
