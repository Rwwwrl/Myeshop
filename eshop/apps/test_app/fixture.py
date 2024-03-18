from sqlalchemy.orm import Session

from eshop import settings
from eshop.apps.test_app.models import Author, Book


def create_data() -> None:
    with Session(settings.SQLALCHEMY_ENGINE) as session:
        author1 = Author(name='author_name')
        book1 = Book(title='title1', author=author1)
        book2 = Book(title='title2', author=author1)

        session.add_all([author1, book1, book2])
        session.commit()


if __name__ == '__main__':
    create_data()
