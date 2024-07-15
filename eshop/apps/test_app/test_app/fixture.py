from test_app.models import Author, Book

from framework.sqlalchemy.session import Session


def create_data() -> None:
    author1 = Author(name='author_name')
    book1 = Book(title='title1', author=author1)
    book2 = Book(title='title2', author=author1)

    with Session() as session:
        with session.begin():
            session.add_all([author1, book1, book2])


if __name__ == '__main__':
    create_data()
