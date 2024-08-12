from typing import List

from sqlalchemy import select

from catalog.domain.models.catalog_type import CatalogType
from catalog.views.http.api_router import api_router

from framework.sqlalchemy.session import Session

from .dto import CatalogTypeDTO

__all__ = ('get_catalog_types', )


def _orm_to_dto(orm: CatalogType) -> CatalogTypeDTO:
    return CatalogTypeDTO(
        id=orm.id,
        type=orm.type,
    )


def _fetch_all_catalog_types_from_db() -> List[CatalogType]:
    with Session() as session:
        with session.begin():
            catalog_types = session.scalars(select(CatalogType)).all()
            session.expunge_all()
            return catalog_types


@api_router.get('/catalog_types/')
def get_catalog_types() -> List[CatalogTypeDTO]:
    return [_orm_to_dto(orm=ct) for ct in _fetch_all_catalog_types_from_db()]
