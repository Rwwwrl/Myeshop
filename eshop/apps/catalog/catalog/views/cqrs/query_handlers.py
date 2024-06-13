from typing import List

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from catalog import hints
from catalog.domain.models import (
    CatalogItem as CatalogItemORM,
)

from catalog_cqrs_contract.query import CatalogItemByIdsQuery
from catalog_cqrs_contract.query.query_response import (
    CatalogBrandDTO,
    CatalogItemDTO,
    CatalogTypeDTO,
)

from framework.cqrs.query import IQueryHandler
from framework.sqlalchemy.session_factory import session_factory

__all__ = ("CatalogItemByIdQueryHandler", )


class NotFoundError(Exception):
    pass


@CatalogItemByIdsQuery.handler
class CatalogItemByIdQueryHandler(IQueryHandler):
    @staticmethod
    def _fetch_from_db(ids: List[hints.CatalogItemId]) -> List[CatalogItemORM]:
        with session_factory() as session:
            # yapf: disable
            stmt = select(
                CatalogItemORM,
            ).where(
                CatalogItemORM.id.in_(ids),
            ).options(
                joinedload(CatalogItemORM.catalog_brand),
                joinedload(CatalogItemORM.catalog_type),
            )
            # yapf: enable
            return session.scalars(stmt).all()

    @staticmethod
    def _to_dto(catalog_item_orm: CatalogItemORM) -> CatalogItemDTO:
        return CatalogItemDTO(
            id=catalog_item_orm.id,
            name=catalog_item_orm.name,
            description=catalog_item_orm.description,
            price=catalog_item_orm.price,
            available_stock=catalog_item_orm.available_stock,
            maxstock_threshold=catalog_item_orm.maxstock_threshold,
            on_reorder=catalog_item_orm.on_reorder,
            picture_filename=catalog_item_orm.picture_filename,
            restock_threshold=catalog_item_orm.restock_threshold,
            picture_url=catalog_item_orm.picture_url,
            catalog_brand=CatalogBrandDTO(
                id=catalog_item_orm.catalog_brand.id,
                brand=catalog_item_orm.catalog_brand.brand,
            ),
            catalog_type=CatalogTypeDTO(
                id=catalog_item_orm.catalog_type.id,
                type=catalog_item_orm.catalog_type.type,
            ),
        )

    def handle(self, query: CatalogItemByIdsQuery) -> CatalogItemDTO:
        return [self._to_dto(ci) for ci in self._fetch_from_db(ids=query.ids)]
