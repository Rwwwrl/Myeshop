from typing import Annotated

from fastapi import Depends, Response, status

from basket.views.http.api_router import api_router

from basket_cqrs_contract.event import UserCheckoutAcceptedEvent
from basket_cqrs_contract.query import CustomerBasketQuery

from framework.fastapi.dependencies.get_user_id_from_http_request import get_user_id_from_http_request

from user_identity_cqrs_contract.hints import UserId
from user_identity_cqrs_contract.query import UserByIdQuery

from .dto import BasketCheckoutRequestData

__all__ = ('checkout', )


@api_router.post('/checkout/')
def checkout(
    request_data: BasketCheckoutRequestData,
    user_id: Annotated[UserId, Depends(get_user_id_from_http_request)],
) -> Response:

    username = UserByIdQuery(id=user_id).fetch().name
    customer_basket = CustomerBasketQuery(customer_id=user_id).fetch()

    event = UserCheckoutAcceptedEvent(
        user_id=user_id,
        username=username,
        order_number=request_data.order_number,
        city=request_data.city,
        street=request_data.street,
        state=request_data.state,
        country=request_data.country,
        zip_code=request_data.zip_code,
        card_number=request_data.card_number,
        card_holder_name=request_data.card_holder_name,
        card_expiration=request_data.card_expiration,
        card_security_number=request_data.card_security_number,
        card_type_id=request_data.card_type_id,
        basket=customer_basket,
    )

    event.publish()

    return Response(status_code=status.HTTP_200_OK)
