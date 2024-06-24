from typing import Annotated, List

from fastapi import Depends, Response, status

import basket_cqrs_contract.command.command
import basket_cqrs_contract.query.query_response
from basket_cqrs_contract.command import UpdateCustomerBasketCommand
from basket_cqrs_contract.query import CustomerBasketQuery

from catalog_cqrs_contract.query import CatalogItemsByIdsQuery

from framework.cqrs.exceptions import CQRSException
from framework.fastapi.dependencies.get_user_from_request import get_user_from_http_request
from framework.fastapi.http_exceptions import InternalServerError

import user_identity_cqrs_contract.hints

from .dto import AddBasketItemRequest
from ..api_router import api_router

__all__ = ('add_basket_item', )


def _to_command_dto(
    basket_item: basket_cqrs_contract.query.query_response.BasketItemDTO,
) -> basket_cqrs_contract.command.command.BasketItemDTO:
    return basket_cqrs_contract.command.command.BasketItemDTO(
        product_id=basket_item.product_id,
        product_name=basket_item.product_name,
        unit_price=basket_item.unit_price,
        quantity=basket_item.quantity,
        picture_url=basket_item.picture_url,
    )


@api_router.post('/basket/basket_items/')
def add_basket_item(
    request_data: AddBasketItemRequest,
    user_id: Annotated[
        user_identity_cqrs_contract.hints.UserId,
        Depends(get_user_from_http_request),
    ],
) -> Response:
    """
    добавляем продукт в корзину:
    1. в случае, если продукт уже есть в корзине, то просто увеличиваем его количество
    2. в случае, если продуакту еще нет, то добавляем его в корзину
    """

    customer_basket = CustomerBasketQuery(customer_id=user_id).fetch()

    try:
        basket_item = next(filter(lambda bi: bi.id == request_data.catalog_item_id, customer_basket.basket_items))
    except StopIteration:
        catalog_item = CatalogItemsByIdsQuery(ids=[request_data.catalog_item_id]).fetch()[0]
        new_basket_item = basket_cqrs_contract.command.command.BasketItemDTO(
            product_id=catalog_item.id,
            product_name=catalog_item.name,
            unit_price=catalog_item.price,
            quantity=request_data.quantity,
            picture_url=catalog_item.picture_url,
        )
        basket_items: List[basket_cqrs_contract.command.command.BasketItemDTO] = [
            new_basket_item,
            *(_to_command_dto(basket_item=bi) for bi in customer_basket.basket_items),
        ]

    else:
        updated_basket_item = basket_cqrs_contract.command.command.BasketItemDTO(
            product_id=basket_item.product_id,
            product_name=basket_item.product_name,
            unit_price=basket_item.unit_price,
            quantity=basket_item.quantity + request_data.quantity,
            picture_url=basket_item.picture_url,
        )
        basket_items: List[basket_cqrs_contract.command.command.BasketItemDTO] = [
            updated_basket_item,
        ]
        for bi in filter(lambda bi: bi.id != basket_item.id, customer_basket.basket_items):
            basket_items.append(_to_command_dto(basket_item=bi))

    try:
        UpdateCustomerBasketCommand(buyer_id=customer_basket.buyer_id, basket_items=basket_items).execute()
    except CQRSException:
        raise InternalServerError(
            detail=f'failed to update basket due to {UpdateCustomerBasketCommand.__name__} failed',
        )

    return Response(status_code=status.HTTP_200_OK)
