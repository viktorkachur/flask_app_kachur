# /run.py

from app import create_app
import os

# ==================================
# ВИПРАВЛЕННЯ ТУТ:
# Зчитуємо FLASK_ENV з .env,
# якщо його немає, використовуємо 'default'
# ==================================
config_name = os.getenv('FLASK_ENV') or 'default'

# Створюємо наш додаток з ПРАВИЛЬНОЮ конфігурацією
app = create_app(config_name)

if __name__ == '__main__':
    app.run()