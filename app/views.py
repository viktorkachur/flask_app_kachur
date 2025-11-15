
from app import application
from flask import render_template


@application.route('/')
def home_page():
    return render_template('resume.html', title="Моє Резюме")

@application.route('/contacts')
def contacts_page():
    return render_template('contacts.html', title="Контакти")