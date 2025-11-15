
from flask_wtf import FlaskForm
from wtforms import (
    StringField, SubmitField, TextAreaField,
    SelectField, PasswordField, BooleanField
)
from wtforms.validators import DataRequired, Length, Email, Regexp


class ContactForm(FlaskForm):
    name = StringField('Ім\'я', [
        DataRequired(message="Це поле є обов'язковим"),
        Length(min=4, max=10, message="Довжина імені має бути від 4 до 10 символів")
    ])

    email = StringField('Email', [
        DataRequired(message="Це поле є обов'язковим"),
        Email(message="Неправильний формат Email")
    ])

    phone = StringField('Телефон', [
        DataRequired(message="Це поле є обов'язковим"),
        Regexp(r'^\+380\d{9}$', message="Формат телефону має бути +380XXXXXXXXX")
    ])

    subject = SelectField('Тема', [
        DataRequired()
    ], choices=[
        ('general', 'Загальне питання'),
        ('support', 'Технічна підтримка'),
        ('feedback', 'Відгук про сайт')
    ])

    message = TextAreaField('Повідомити', [
        DataRequired(message="Це поле є обов'язковим"),
        Length(max=500, message="Повідомлення не може перевищувати 500 символів")
    ])

    submit = SubmitField('Надіслати')

class LoginForm(FlaskForm):

    username = StringField('Ім\'я користувача', [
        DataRequired(message="Це поле є обов'язковим")
    ])

    password = PasswordField('Пароль', [
        DataRequired(message="Це поле є обов'язковим"),
        Length(min=4, max=10, message="Пароль має бути від 4 до 10 символів")
    ])

    remember = BooleanField('Запам\'ятати мене')

    submit = SubmitField('Увійти')