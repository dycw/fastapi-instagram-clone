from typing import cast

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from fastapi_instagram_clone.db.database import Base


class DbUser(Base):
    __tablename__ = "users"

    id = cast(int, Column(Integer, primary_key=True, index=True))
    username = cast(str, Column(String))
    email = cast(str, Column(String))
    password = cast(str, Column(String))
    items = relationship("DbArticle", back_populates="user")


class DbArticle(Base):
    __tablename__ = "articles"

    id = cast(int, Column(Integer, primary_key=True, index=True))
    title = cast(str, Column(String))
    content = cast(str, Column(String))
    published = cast(bool, Column(Boolean))
    user_id = cast(int, Column(Integer, ForeignKey("users.id")))
    user = relationship("DbUser", back_populates="items")
