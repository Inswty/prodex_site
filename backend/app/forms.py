from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    """Форма обратной связи."""

    name = StringField('Имя', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Телефон', validators=[Length(max=30)])
    message = TextAreaField(
        'Сообщение', validators=[DataRequired(), Length(max=1000)]
    )
    submit = SubmitField('Отправить')
