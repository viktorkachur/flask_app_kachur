from flask import (
    render_template, request, url_for, redirect,
    flash, session, make_response
)
from app.users import users_bp
from app.forms import LoginForm  # Зверни увагу: тут НЕМАЄ ContactForm
import datetime



@users_bp.route("/hi/<string:name>")
def greetings(name):
    age = request.args.get("age", None)
    processed_name = name.upper()
    return render_template("users/hi.html",
                           name=processed_name,
                           age=age)


@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45)
    return redirect(to_url)



@users_bp.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        all_cookies = request.cookies
        theme = request.cookies.get('theme', 'light')
        return render_template(
            'users/profile.html',
            username=username,
            all_cookies=all_cookies,
            theme=theme
        )
    else:
        flash('Ви повинні увійти, щоб побачити цю сторінку.', 'warning')
        return redirect(url_for('users.login'))


@users_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('Ви успішно вийшли з системи.', 'info')
    return redirect(url_for('users.login'))


@users_bp.route('/cookie/add', methods=['POST'])
def add_cookie():
    if 'username' not in session:
        flash('Доступ заборонено.', 'danger')
        return redirect(url_for('users.login'))
    key = request.form.get('cookie_key')
    value = request.form.get('cookie_value')
    expiry = request.form.get('cookie_expiry')
    if not key or not value:
        flash('Ключ та значення кукі є обов\'язковими.', 'warning')
        return redirect(url_for('users.profile'))
    response = make_response(redirect(url_for('users.profile')))
    try:
        if expiry:
            expiry_seconds = int(expiry)
            expires_at = datetime.datetime.now() + datetime.timedelta(seconds=expiry_seconds)
            response.set_cookie(key, value, expires=expires_at)
        else:
            response.set_cookie(key, value)
        flash(f'Кукі "{key}" успішно додано.', 'success')
    except Exception as e:
        flash(f'Помилка при додаванні кукі: {e}', 'danger')
    return response


@users_bp.route('/cookie/delete', methods=['POST'])
def delete_cookie():
    if 'username' not in session:
        flash('Доступ заборонено.', 'danger')
        return redirect(url_for('users.login'))
    key_to_delete = request.form.get('cookie_key_to_delete')
    if not key_to_delete:
        flash('Ви не вказали ключ кукі для видалення.', 'warning')
        return redirect(url_for('users.profile'))
    response = make_response(redirect(url_for('users.profile')))
    response.set_cookie(key_to_delete, '', expires=0)
    flash(f'Кукі "{key_to_delete}" успішно видалено.', 'success')
    return response


@users_bp.route('/cookie/delete_all', methods=['POST'])
def delete_all_cookies():
    if 'username' not in session:
        flash('Доступ заборонено.', 'danger')
        return redirect(url_for('users.login'))
    response = make_response(redirect(url_for('users.profile')))
    keys_to_delete = []
    for key in request.cookies:
        if key != 'session':
            response.set_cookie(key, '', expires=0)
            keys_to_delete.append(key)
    flash(f'Успішно видалено {len(keys_to_delete)} кукі.', 'success')
    return response


@users_bp.route('/set-theme/<theme>')
def set_theme(theme):
    if 'username' not in session:
        return redirect(url_for('users.login'))
    response = make_response(redirect(url_for('users.profile')))
    max_age = 60 * 60 * 24 * 30
    response.set_cookie('theme', theme, max_age=max_age)
    return response


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        flash('Ви вже увійшли в систему.', 'info')
        return redirect(url_for('users.profile'))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        if username == 'user' and password == 'pass':
            session['username'] = username

            remember_message = "з опцією 'Запам'ята...'" if remember else "без опції 'Запам'я...'"
            flash(f'Вхід успішний! Вітаємо, {username} ({remember_message}).', 'success')

            return redirect(url_for('users.profile'))
        else:
            flash('Неправильне ім\'я користувача або пароль.', 'danger')
            return redirect(url_for('users.login'))

    return render_template('users/login.html', form=form)