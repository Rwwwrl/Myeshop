from attrs import define

from catalog_cqrs_contract import hints

from framework.cqrs.query.query import Query

from .query_response import CatalogItemDTO

__all__ = ('CatalogItemByIdQuery', )


@define
class CatalogItemByIdQuery(Query[CatalogItemDTO]):

    id: hints.CatalogItemId
