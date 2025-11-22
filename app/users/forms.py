from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Ім\'я користувача', validators=[
        DataRequired(),
        Length(min=4, max=20, message="Ім'я має бути від 4 до 20 символів")
    ])

    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Некоректний email")
    ])

    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=6, message="Пароль має бути мінімум 6 символів")
    ])

    confirm_password = PasswordField('Підтвердіть пароль', validators=[
        DataRequired(),
        EqualTo('password', message="Паролі повинні співпадати")
    ])

    submit = SubmitField('Зареєструватися')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Це ім\'я вже зайняте. Будь ласка, оберіть інше.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Цей email вже зареєстрований.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Некоректний email")
    ])

    password = PasswordField('Пароль', validators=[
        DataRequired()
    ])

    remember = BooleanField('Запам\'ятати мене')

    submit = SubmitField('Увійти')
