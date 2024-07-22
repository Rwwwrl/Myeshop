from typing import List

from sqlalchemy import select

from catalog.api_router import api_router
from catalog.infrastructure.persistance.postgres.models import CatalogBrandORM

from framework.sqlalchemy.session import Session

from .dto import CatalogBrandDTO

__all__ = ('get_catalog_brands', )


def _orm_to_dto(orm: CatalogBrandORM) -> CatalogBrandDTO:
    return CatalogBrandDTO(
        id=orm.id,
        brand=orm.brand,
    )


def _fetch_all_catalog_brands_from_db() -> List[CatalogBrandORM]:
    with Session() as session:
        with session.begin():
            catalog_brands = session.scalars(select(CatalogBrandORM)).all()
            session.expunge_all()
            return catalog_brands


@api_router.get('/catalog_brands/')
def get_catalog_brands() -> List[CatalogBrandDTO]:
    return [_orm_to_dto(orm=ct) for ct in _fetch_all_catalog_brands_from_db()]
