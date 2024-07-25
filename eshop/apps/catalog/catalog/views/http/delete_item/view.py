from fastapi import Response, status

from sqlalchemy import delete, text
from sqlalchemy.orm import Session as lib_Session

from catalog import hints
from catalog.api_router import api_router
from catalog.infrastructure.persistance.postgres.models import CatalogItemORM

from catalog_cqrs_contract.event import CatalogItemHasBeenDeleted

from framework.sqlalchemy.session import Session

__all__ = ('delete_item', )


def _check_if_catalog_item_exists(session: lib_Session, catalog_item_id: hints.CatalogItemId) -> bool:
    stmt = text('SELECT EXISTS(SELECT 1 from catalog.catalog_item WHERE id = :id);')
    return session.scalar(stmt, params={'id': catalog_item_id})


def _delete_catalog_item_from_db(session: lib_Session, catalog_item_id: hints.CatalogItemId) -> None:
    stmt = delete(CatalogItemORM).where(CatalogItemORM.id == catalog_item_id)
    session.execute(stmt)


# TODO: доступ к эндпоинту должен иметь только админ
@api_router.delete('/items/')
def delete_item(catalog_item_id: hints.CatalogItemId) -> Response:
    with Session() as session:
        with session.begin():
            is_catalog_item_exists = _check_if_catalog_item_exists(
                session=session,
                catalog_item_id=catalog_item_id,
            )

    if is_catalog_item_exists:
        event = CatalogItemHasBeenDeleted(id=catalog_item_id)
        with Session() as session:
            with session.begin():
                _delete_catalog_item_from_db(session=session, catalog_item_id=catalog_item_id)
                # TODO реализовать обработчик
                event.publish()

    return Response(status_code=status.HTTP_200_OK)
