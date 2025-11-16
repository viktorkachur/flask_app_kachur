from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, DateTime, Enum, Boolean
import enum


class PostCategory(enum.Enum):
    news = "Новина"
    publication = "Публікація"
    tech = "Технології"
    other = "Інше"


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    category: Mapped[PostCategory] = mapped_column(
        Enum(PostCategory),
        default=PostCategory.other
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    author: Mapped[str] = mapped_column(String(20), default='Anonymous')


    def __repr__(self):
        return f'<Post(title={self.title})>'