
from flask import Flask, render_template

web_app = Flask(__name__)


@web_app.route('/')
def home_page():

    return render_template('resume.html', title="Моє Резюме")

@web_app.route('/contacts')
def contacts_page():

    return render_template('contacts.html', title="Контакти")
if __name__ == '__main__':
    web_app.run(debug=True)