from typing import final

from attrs import define

from basket_cqrs_contract.customer_basket_dto import CustomerBasketDTO

from framework.cqrs.command import SyncCommand

__all__ = ('UpdateCustomerBasketCommand', )


@final
@define
class UpdateCustomerBasketCommand(SyncCommand[None]):

    customer_basket: CustomerBasketDTO
