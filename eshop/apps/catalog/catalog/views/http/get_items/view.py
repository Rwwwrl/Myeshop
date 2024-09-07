from typing import Annotated, List, Optional

from fastapi import Query

from sqlalchemy import select

from catalog import hints
from catalog.domain.models import CatalogItem
from catalog.views.http.api_router import api_router

from framework.fastapi.http_exceptions import BadRequestException
from framework.sqlalchemy.session import Session

from ..common.catalog_item_dto import CatalogItemDTO

__all__ = ('get_items', )


def _parse_request_ids(ids: str) -> List[hints.CatalogItemId]:
    import ast

    ids = ast.literal_eval(ids)

    if not isinstance(ids, list):
        raise ValueError

    for id in ids:
        if not isinstance(id, int):
            raise ValueError

    return ids


def _fetch_catalog_items_from_db(ids: Optional[List[hints.CatalogItemId]]) -> List[CatalogItem]:
    if ids:
        stmt = select(CatalogItem).where(CatalogItem.id.in_(ids))
    else:
        stmt = select(CatalogItem)

    with Session() as session:
        with session.begin():
            catalog_items = session.scalars(stmt).all()
            session.expunge_all()
            return catalog_items


@api_router.get('/items/')
def get_items(ids: Annotated[Optional[str], Query(example='[10, 20, 30]')] = None) -> List[CatalogItemDTO]:
    # TODO: добавить пагинацию в случае если не передается ids
    if ids:
        try:
            ids = _parse_request_ids(ids=ids)
        except ValueError:
            raise BadRequestException(detail='invalid query parameter "ids", must be a list of int')

    return [CatalogItemDTO.from_orm(orm=ci) for ci in _fetch_catalog_items_from_db(ids=ids)]
