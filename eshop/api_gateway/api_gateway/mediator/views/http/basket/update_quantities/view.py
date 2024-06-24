from typing import Annotated, Dict, List

from fastapi import Depends, Response, status

import basket_cqrs_contract.command.command
import basket_cqrs_contract.hints
import basket_cqrs_contract.query.query_response
from basket_cqrs_contract.command import UpdateCustomerBasketCommand
from basket_cqrs_contract.query.query import CustomerBasketQuery

from framework.cqrs.exceptions import CQRSException
from framework.fastapi.dependencies.get_user_from_request import get_user_from_http_request
from framework.fastapi.http_exceptions import BadRequestException
from framework.fastapi.http_exceptions import InternalServerError

import user_identity_cqrs_contract.hints

from .dto import UpdateBasketItemsRequest
from ..api_router import api_router

__all__ = ('update_quantities', )


@api_router.put('/basket/basket_items/')
def update_quantities(
    request_data: UpdateBasketItemsRequest,
    user_id: Annotated[
        user_identity_cqrs_contract.hints.UserId,
        Depends(get_user_from_http_request),
    ],
) -> Response:
    if not request_data.updates:
        raise BadRequestException(detail='no updates sent')

    customer_basket = CustomerBasketQuery(customer_id=user_id).fetch()

    CustomerBasketBasketItemsIdentityMap = (
        Dict[
            basket_cqrs_contract.hints.BasketItemId,
            basket_cqrs_contract.query.query_response.BasketItemDTO,
        ]
    )
    customer_basket_basket_items_identity_map: CustomerBasketBasketItemsIdentityMap = {}
    for basket_item in customer_basket.basket_items:
        customer_basket_basket_items_identity_map[basket_item.id] = basket_item

    updated_basket_items: List[basket_cqrs_contract.command.command.BasketItemDTO] = []
    for update_basket_item_data in request_data.updates:
        basket_item = customer_basket_basket_items_identity_map[update_basket_item_data.basket_item_id]
        updated_basket_items.append(
            basket_cqrs_contract.command.command.BasketItemDTO(
                product_id=basket_item.product_id,
                product_name=basket_item.product_name,
                unit_price=basket_item.unit_price,
                quantity=update_basket_item_data.new_quantity,
                picture_url=basket_item.picture_url,
            ),
        )

    try:
        UpdateCustomerBasketCommand(
            buyer_id=user_id,
            basket_items=updated_basket_items,
        ).execute()
    except CQRSException:
        raise InternalServerError(
            detail=f'failed to update basket due to {UpdateCustomerBasketCommand.__name__} failed',
        )

    return Response(status_code=status.HTTP_200_OK)
