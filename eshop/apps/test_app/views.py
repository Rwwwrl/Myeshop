from sqlalchemy import select
from sqlalchemy.orm import Session

from eshop import settings
from eshop.apps.test_app import hints

from framework.ddd.dto import DTO

from .api_router import api_router
from .models import Author, Book


@api_router.get('/index/')
def index():
    return {'hello': 'world'}


@api_router.get('/settings/')
def settings__get():
    from eshop.settings import SETTINGS

    return {'db_name': SETTINGS.db.name}


class BookDTO(DTO):

    title: str
    author_name: str


@api_router.get('/book/{id}/')
def book__get(id: hints.BookId) -> BookDTO:
    with Session(settings.SQLALCHEMY_ENGINE) as session:
        # yapf: disable
        stmt = select(
            Book.title.label('title'),
            Author.name.label('author_name'),
        ).select_from(
            Book,
        ).join(
            Author,
        ).where(
            Book.id == id,
        )
        # yapf: enable
        result = session.execute(stmt).one()._asdict()

    return BookDTO(title=result['title'], author_name=result['author_name'])


class ToTestLoggingSerializationInnerDTO(DTO):

    value1: str
    value2: int


class ToTestLoggingSerializationDTO(DTO):
    value1: str
    value2: int
    inner_dto: ToTestLoggingSerializationInnerDTO


@api_router.get('/test/')
def test() -> dict:
    import logging

    logger = logging.getLogger('test_app.views.test')

    logger.debug('some debug info')
    logger.warning('some warning!')

    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception('some exception info')

    dto = ToTestLoggingSerializationDTO(
        value1='value1',
        value2=10,
        inner_dto=ToTestLoggingSerializationInnerDTO(
            value1='value1_inner',
            value2=20,
        ),
    )

    logger.debug('invalid dto: %s', dto)

    return {"hello": "world"}
