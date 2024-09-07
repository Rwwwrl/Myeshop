from typing import List

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from catalog import hints
from catalog.domain.models import CatalogItem

from catalog_cqrs_contract.query import CatalogItemsByIdsQuery
from catalog_cqrs_contract.query.query_response import (
    CatalogBrandDTO,
    CatalogItemDTO,
    CatalogTypeDTO,
)

from framework.cqrs.query import IQueryHandler
from framework.sqlalchemy.session import Session

__all__ = ('CatalogItemByIdQueryHandler', )


@CatalogItemsByIdsQuery.handler
class CatalogItemByIdQueryHandler(IQueryHandler):
    @staticmethod
    def _fetch_from_db(ids: List[hints.CatalogItemId]) -> List[CatalogItem]:
        with Session() as session:
            # yapf: disable
            stmt = select(
                CatalogItem,
            ).where(
                CatalogItem.id.in_(ids),
            ).options(
                joinedload(CatalogItem.catalog_brand),
                joinedload(CatalogItem.catalog_type),
            )
            # yapf: enable
            with session.begin():
                catalog_items = session.scalars(stmt).all()
                session.expunge_all()
                return catalog_items

    @staticmethod
    def _to_dto(catalog_item_orm: CatalogItem) -> CatalogItemDTO:
        return CatalogItemDTO(
            id=catalog_item_orm.id,
            name=catalog_item_orm.name,
            description=catalog_item_orm.description,
            price=catalog_item_orm.price,
            discount=catalog_item_orm.discount,
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

    def handle(self, query: CatalogItemsByIdsQuery) -> CatalogItemDTO:
        return [self._to_dto(ci) for ci in self._fetch_from_db(ids=query.ids)]
