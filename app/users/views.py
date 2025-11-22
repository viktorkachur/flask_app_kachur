from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import db, bcrypt
from app.users.forms import RegistrationForm, LoginForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from . import users_bp

@users_bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts.all_posts'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Акаунт створено для {form.username.data}! Тепер ви можете увійти.', 'success')
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


@users_bp.route("/account")
@login_required
def account():
    return render_template('users/account.html', title='Account')