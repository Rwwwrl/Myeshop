from attrs import define

from basket_cqrs_contract import hints

from framework.cqrs.query.query import Query

from .query_response import CustomerBasketDTO

__all__ = ('BasketByIdQuery', )


@define
class BasketByIdQuery(Query[CustomerBasketDTO]):
    id: hints.CustomerBasketId
