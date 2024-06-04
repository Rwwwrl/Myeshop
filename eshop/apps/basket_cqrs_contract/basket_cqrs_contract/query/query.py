from basket_cqrs_contract import hints

from framework.cqrs.query.query import Query, query

from .query_response import BasketDTO

__all__ = ('BasketByIdQuery', )


@query(BasketDTO)
class BasketByIdQuery(Query):
    id: hints.CustomerBasketId
