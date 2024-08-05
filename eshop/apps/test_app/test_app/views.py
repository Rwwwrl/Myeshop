from fastapi import Response, UploadFile as fastapi_UploadFile, status

from sqlalchemy import select

from test_app import hints

from framework.common.dto import DTO
from framework.file_storage import UploadFile
from framework.file_storage.local_file_storage.local_file_storage_maker import LocalFileStorage
from framework.sqlalchemy.session import Session

from .api_router import api_router
from .models import Author, Book


@api_router.get('/index/')
def index():
    return {'hello': 'world'}


@api_router.get('/settings/')
def settings__get():
    from eshop.settings import SETTINGS

    return {'db_name': SETTINGS.postgres.name}


class BookDTO(DTO):

    title: str
    author_name: str


@api_router.get('/book/{id}/')
def book__get(id: hints.BookId) -> BookDTO:
    with Session() as session:
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
        with session.begin():
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


@api_router.post('/file_upload/')
def test_file_upload(upload_file: fastapi_UploadFile) -> Response:
    LocalFileStorage().upload(
        upload_file=UploadFile(file=upload_file.file, filename=upload_file.filename),
        space='test_app',
    )
    return Response(status_code=status.HTTP_200_OK)


class TestRequestBodyWithFileBody(DTO):
    message: str


@api_router.post('/test_request_body_with_file/')
def test_request_body_with_file(upload_file: fastapi_UploadFile, body: TestRequestBodyWithFileBody) -> Response:
    return Response(status_code=status.HTTP_200_OK)
