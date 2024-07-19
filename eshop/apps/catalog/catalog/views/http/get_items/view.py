from typing import Annotated, List, Optional

from fastapi import Query

from sqlalchemy import select

from catalog import hints
from catalog.api_router import api_router
from catalog.infrastructure.persistance.postgres.models import CatalogItemORM

from framework.fastapi.http_exceptions import BadRequestException
from framework.sqlalchemy.session import Session

from .dto import CatalogItemDTO

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


def _fetch_catalog_items_from_db(ids: Optional[List[hints.CatalogItemId]]) -> List[CatalogItemORM]:
    if ids:
        stmt = select(CatalogItemORM).where(CatalogItemORM.id.in_(ids))
    else:
        stmt = select(CatalogItemORM)

    with Session() as session:
        with session.begin():
            catalog_items = session.scalars(stmt).all()
            session.expunge_all()
            return catalog_items


def _orm_to_dto(orm: CatalogItemORM) -> CatalogItemDTO:
    return CatalogItemDTO(
        id=orm.id,
        name=orm.name,
        description=orm.description,
        price=orm.price,
        picture_filename=orm.picture_filename,
        picture_url=orm.picture_url,
        catalog_type_id=orm.catalog_type_id,
        catalog_brand_id=orm.catalog_brand_id,
        available_stock=orm.available_stock,
        restock_threshold=orm.restock_threshold,
        maxstock_threshold=orm.maxstock_threshold,
        on_reorder=orm.on_reorder,
    )


@api_router.get('/items/')
def get_items(ids: Annotated[Optional[str], Query(example="[10, 20, 30]")] = None) -> List[CatalogItemDTO]:
    # TODO: добавить пагинацию в случае если не передается ids
    if ids:
        try:
            ids = _parse_request_ids(ids=ids)
        except ValueError:
            raise BadRequestException(detail='invalid query parameter "ids", must be a list of int')

        return [_orm_to_dto(ci) for ci in _fetch_catalog_items_from_db(ids=ids)]

    return [_orm_to_dto(ci) for ci in _fetch_catalog_items_from_db()]
