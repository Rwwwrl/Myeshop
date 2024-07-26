from typing import List, final

from attrs import define

from catalog_cqrs_contract import hints

from framework.cqrs.query.query import Query

from .query_response import CatalogItemDTO

__all__ = ('CatalogItemsByIdsQuery', )


@final
@define
class CatalogItemsByIdsQuery(Query[List[CatalogItemDTO]]):

    ids: List[hints.CatalogItemId]
