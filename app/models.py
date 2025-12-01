# /app/models.py

from . import db, bcrypt, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime  # <-- Додано DateTime
from typing import List, Optional  # <-- Додано Optional
from datetime import datetime  # <-- Додано datetime


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)

    image_file: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default='default.jpg',
        server_default='default.jpg'
    )

    # --- НОВІ ПОЛЯ (Завдання 6) ---
    about_me: Mapped[Optional[str]] = mapped_column(String(140))
    last_seen: Mapped[Optional[datetime]] = mapped_column(DateTime)
    # -----------------------------

    posts: Mapped[List["Post"]] = relationship("Post", back_populates="user", cascade="all, delete-orphan")

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"