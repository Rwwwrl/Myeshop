from sqlalchemy import ForeignKey, Integer, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from test_app import hints
from test_app.app_config import TestAppConfig


class Base(DeclarativeBase):
    metadata = MetaData(schema=TestAppConfig.name)


class Author(Base):

    __tablename__ = 'author'

    id: Mapped[hints.AuthorId] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column()

    books: Mapped[list['Book']] = relationship(back_populates='author')


class Book(Base):

    __tablename__ = 'book'

    id: Mapped[hints.BookId] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column()
    author_id: Mapped[hints.AuthorId] = mapped_column(ForeignKey(f'{Author.__tablename__}.id'))

    author: Mapped[Author] = relationship(back_populates='books')
