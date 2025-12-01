# /app/users/views.py

import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, current_app
from app import db, bcrypt
from app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, ChangePasswordForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from . import users_bp
from datetime import datetime  # <-- Потрібно для часу


# --- НОВА ФУНКЦІЯ (Завдання 6) ---
# Виконується перед кожним запитом до сайту
@users_bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        # Ми не робимо тут full commit, щоб не перевантажувати базу,
        # але для лаби зробимо commit
        db.session.commit()


# --------------------------------

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@users_bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts.all_posts'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Акаунт створено для {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', title='Register', form=form)


@users_bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.all_posts'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(db.select(User).where(User.email == form.email.data))
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Ви успішно увійшли!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('users.account'))
        else:
            flash('Вхід не вдався. Перевірте email та пароль.', 'danger')
    return render_template('users/login.html', title='Login', form=form)


@users_bp.route("/logout")
def logout():
    logout_user()
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('posts.all_posts'))


@users_bp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        # Зберігаємо "Про себе"
        current_user.about_me = form.about_me.data

        db.session.commit()
        flash('Ваш акаунт оновлено!', 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        # Заповнюємо поле "Про себе"
        form.about_me.data = current_user.about_me

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('users/account.html', title='Account',
                           image_file=image_file, form=form)


# --- НОВИЙ МАРШРУТ (Завдання 7) ---
@users_bp.route("/account/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        # 1. Перевіряємо, чи правильний старий пароль
        if current_user.verify_password(form.current_password.data):
            # 2. Хешуємо та зберігаємо новий пароль (сетер password зробить хешування)
            current_user.password = form.new_password.data
            db.session.commit()

            flash('Ваш пароль успішно змінено! Увійдіть з новим паролем.', 'success')
            # Для безпеки можна розлогінити користувача, але це не обов'язково.
            # Ми просто перенаправимо на профіль.
            return redirect(url_for('users.account'))
        else:
            flash('Невірний поточний пароль.', 'danger')

    return render_template('users/change_password.html', title='Change Password', form=form)