# /app/users/forms.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField  # <-- Додано TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Ім\'я користувача', validators=[
        DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[
        DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[
        DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Підтвердіть пароль', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Зареєструватися')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Це ім\'я вже зайняте.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Цей email вже зареєстрований.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запам\'ятати мене')
    submit = SubmitField('Увійти')


class UpdateAccountForm(FlaskForm):
    username = StringField('Ім\'я користувача', validators=[
        DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[
        DataRequired(), Email()])

    # --- НОВЕ ПОЛЕ ---
    about_me = TextAreaField('Про себе', validators=[Length(max=140)])
    # -----------------

    picture = FileField('Оновити фото профілю', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Тільки зображення!')
    ])

    submit = SubmitField('Оновити')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Це ім\'я вже зайняте.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Цей email вже зареєстрований.')

# --- НОВА ФОРМА (Завдання 7) ---
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Поточний пароль', validators=[DataRequired()])
    new_password = PasswordField('Новий пароль', validators=[
        DataRequired(),
        Length(min=6, message="Пароль має бути мінімум 6 символів")
    ])
    confirm_password = PasswordField('Підтвердіть новий пароль', validators=[
        DataRequired(),
        EqualTo('new_password', message="Паролі повинні співпадати")
    ])
    submit = SubmitField('Змінити пароль')