from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, Enum, Boolean, ForeignKey, Table
from sqlalchemy.sql import func
from typing import List
import enum
import datetime

post_tags = db.Table(
    'post_tags',
    db.Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class PostCategory(enum.Enum):
    news = "Новина"
    publication = "Публікація"
    tech = "Технології"
    other = "Інше"


class Tag(db.Model):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    posts: Mapped[List["Post"]] = relationship(
        secondary=post_tags,
        back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag {self.name}>"


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    category: Mapped[PostCategory] = mapped_column(Enum(PostCategory), default=PostCategory.other)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="posts")

    tags: Mapped[List["Tag"]] = relationship(
        secondary=post_tags,
        back_populates="posts"
    )

    def __repr__(self):
        return f'<Post(title={self.title})>'