from attrs import define

from basket_cqrs_contract import hints

from framework.cqrs.query.query import Query

from .query_response import CustomerBasketDTO

__all__ = ('CustomerBasketQuery', )


@define
class CustomerBasketQuery(Query[CustomerBasketDTO]):
    customer_id: hints.CustomerId
