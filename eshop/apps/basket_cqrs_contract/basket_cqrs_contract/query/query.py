from typing import final

from attrs import define

from basket_cqrs_contract import hints

from framework.cqrs.exceptions import PossibleExpectedError
from framework.cqrs.query.query import Query

from .query_response import CustomerBasketDTO

__all__ = ('CustomerBasketQuery', )


@final
class CustomerDoesNotHaveBasketError(PossibleExpectedError):
    pass


@final
@define
class CustomerBasketQuery(Query[CustomerBasketDTO]):
    customer_id: hints.CustomerId

    __possible_exceptions__ = (CustomerDoesNotHaveBasketError, )
