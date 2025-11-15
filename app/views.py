from flask import render_template, flash, redirect, url_for
from app import application
from app.forms import ContactForm
from loguru import logger


logger.add("contact.log",
           format="{time} {level} {message}",
           level="INFO",
           rotation="10 MB",
           compression="zip")



@application.route('/')
def home_page():

    return render_template('resume.html', title="Моє Резюме")


@application.route('/contacts', methods=['GET', 'POST'])
def contacts_page():

    form = ContactForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = form.subject.data
        message = form.message.data

        logger.info(f"New contact message from {name} ({email}). "
                    f"Phone: {phone}, Subject: {subject}, "
                    f"Message: {message}")

        flash(f'Дякуємо, {name}! Ваше повідомлення на тему "{subject}" було успішно надіслано.', 'success')

        return redirect(url_for('contacts_page'))

    return render_template('contacts.html', title="Контакти", form=form)