from eshop import settings
from eshop.apps.test_app import hints
from eshop.apps.test_app.app_config import TestAppConfig

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Author(settings.SQLALCHEMY_BASE):

    __tablename__ = f'{TestAppConfig.name}__author'

    id: Mapped[hints.AuthorId] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column()

    books: Mapped[list['Book']] = relationship(back_populates='author')


class Book(settings.SQLALCHEMY_BASE):

    __tablename__ = f'{TestAppConfig.name}__book'

    id: Mapped[hints.BookId] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column()
    author_id: Mapped[hints.AuthorId] = mapped_column(ForeignKey(f'{Author.__tablename__}.id'))

    author: Mapped[Author] = relationship(back_populates='books')
