from flask_wtf import FlaskForm
from wtforms import (
    StringField, SubmitField, TextAreaField,
    SelectField, BooleanField, DateTimeLocalField,
    SelectMultipleField
)
from wtforms.validators import DataRequired, Length
from app.posts.models import PostCategory
import datetime

CATEGORIES = [
    (cat.name, cat.value) for cat in PostCategory
]


class PostForm(FlaskForm):
    title = StringField("Заголовок", [
        DataRequired(),
        Length(min=2, message="Заголовок має бути довшим")
    ])

    content = TextAreaField("Вміст", [
        DataRequired()
    ], render_kw={"rows": 5})

    is_active = BooleanField('Активний пост', default=True)

    publish_date = DateTimeLocalField('Дата публікації',
                                      format="%Y-%m-%dT%H:%M",
                                      default=datetime.datetime.now)

    category = SelectField('Категорія',
                           choices=CATEGORIES,
                           validators=[DataRequired()])

    author_id = SelectField("Автор", coerce=int)
    tags = SelectMultipleField("Теги", coerce=int)

    submit = SubmitField("Опублікувати")