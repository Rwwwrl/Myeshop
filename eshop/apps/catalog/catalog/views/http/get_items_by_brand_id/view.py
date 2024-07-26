from typing import List

from sqlalchemy import select

from catalog import hints
from catalog.api_router import api_router
from catalog.infrastructure.persistance.postgres import CatalogItemORM

from framework.sqlalchemy.session import Session

from ..common.catalog_item_dto import CatalogItemDTO

__all__ = ('get_items_by_brand_id', )


def _fetch_catalog_items_from_db(brand_id: hints.CatalogBrandId) -> List[CatalogItemORM]:
    # yapf: disable
    stmt = select(
        CatalogItemORM,
    ).where(
        CatalogItemORM.catalog_brand_id == brand_id,
    )
    # yapf: enable

    with Session() as session:
        with session.begin():
            catalog_items = session.scalars(stmt).all()
            session.expunge_all()
            return catalog_items


@api_router.get('/items/type/all/brand/{brand_id}/')
def get_items_by_brand_id(brand_id: hints.CatalogBrandId) -> List[CatalogItemDTO]:
    # TODO: добавить пагинацию
    catalog_items = _fetch_catalog_items_from_db(brand_id=brand_id)
    return [CatalogItemDTO.from_orm(orm=ci) for ci in catalog_items]
