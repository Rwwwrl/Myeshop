from collections import defaultdict
from typing import Annotated, Dict, List, Set

from fastapi import status
from fastapi.responses import Response

from basket_cqrs_contract.command import UpdateCustomerBasketCommand
from basket_cqrs_contract.command.command import BasketItemDTO

import catalog_cqrs_contract.hints
from catalog_cqrs_contract.query import CatalogItemByIdsQuery
from catalog_cqrs_contract.query.query_response import CatalogItemDTO

from framework.cqrs.cqrs_bus import CQRSException
from framework.fastapi.dependencies.get_user_from_request import get_user_from_http_request
from framework.fastapi.http_exceptions import BadRequestException, InternalServerError

import user_identity_cqrs_contract.hints

from .dto import ProductId, UpdateBasketRequestData, UpdateBasketRequestItemData
from ..api_router import api_router

__all__ = ('update_basket', )


class BasketReferToNonExisingProducts(Exception):
    def __init__(self, *args, invalid_product_ids: List[ProductId], **kwargs):
        self.invalid_product_ids = invalid_product_ids


def _normalize_request_data(request_data: UpdateBasketRequestData) -> UpdateBasketRequestData:
    """
    группируем дату по `product_id` во избежание дубликатов
    """

    product_it_to_quantity: Dict[int, int] = defaultdict(float)

    for basket_item in request_data.basket_items:
        product_it_to_quantity[basket_item.product_id] += basket_item.quantity

    return UpdateBasketRequestData(
        buyer_id=request_data.buyer_id,
        basket_items=[
            UpdateBasketRequestItemData(
                product_id=product_id,
                quantity=quantity,
            ) for product_id, quantity in product_it_to_quantity.items()
        ],
    )


def _ensure_basket_refer_to_existing_products(
    request_data: UpdateBasketRequestData,
    existing_products_ids: Set[ProductId],
) -> None:
    invalid_product_ids: List[int] = []

    for product_id in [bi.product_id for bi in request_data.basket_items]:
        if product_id not in existing_products_ids:
            invalid_product_ids.append(product_id)

    if invalid_product_ids:
        raise BasketReferToNonExisingProducts(invalid_product_ids=invalid_product_ids)


# TODO добавить статусы ошибок
@api_router.put(
    '/basket/',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'success',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'unauthorized',
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'basket refer to non-existing products',
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR:
            {
                'description': 'failed to update basket due to UpdateCustomerBasketCommand failed',
            },
    },
)
def update_basket(
    request_data: UpdateBasketRequestData,
    user_id: Annotated[user_identity_cqrs_contract.hints.UserId, get_user_from_http_request],
) -> None:
    if not request_data.basket_items:
        raise BadRequestException(detail='basket must have at least one basket item')

    request_data = _normalize_request_data(request_data=request_data)
    request_data_product_ids: List[int] = [bi.product_id for bi in request_data.basket_items]

    catalog_items = CatalogItemByIdsQuery(ids=request_data_product_ids).fetch()
    catalog_items_identity_map: Dict[catalog_cqrs_contract.hints.CatalogItemId, CatalogItemDTO] = {
        item.id: item
        for item in catalog_items
    }

    try:
        _ensure_basket_refer_to_existing_products(
            request_data=request_data,
            existing_products_ids=set(ProductId(item.id) for item in catalog_items),
        )
    except BasketReferToNonExisingProducts as e:
        raise BadRequestException(
            detail=f'basket refer to non-existing products, invalid products: {e.invalid_product_ids}',
        )

    basket_updated_basket_items: List[BasketItemDTO] = []
    for basket_request_item_data in request_data.basket_items:
        product_id = basket_request_item_data.product_id
        basket_updated_basket_items.append(
            BasketItemDTO(
                product_id=basket_request_item_data.product_id,
                product_name=catalog_items_identity_map[product_id].name,
                unit_price=catalog_items_identity_map[product_id].price,
                quantity=basket_request_item_data.quantity,
                picture_url=catalog_items_identity_map[product_id].picture_url,
            ),
        )

    try:
        UpdateCustomerBasketCommand(buyer_id=user_id, basket_items=basket_updated_basket_items).execute()
    except CQRSException:
        raise InternalServerError(detail='failed to update basket due to UpdateCustomerBasketCommand failed')

    return Response(status_code=status.HTTP_200_OK)
