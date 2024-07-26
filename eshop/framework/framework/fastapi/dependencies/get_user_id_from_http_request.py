from typing import Annotated

from fastapi import Depends

from user_identity_cqrs_contract.hints import UserId
from user_identity_cqrs_contract.query.query_response import UserIdWithRoleDTO

from .get_user_from_http_request import get_user_from_http_request


def get_user_id_from_http_request(user: Annotated[UserIdWithRoleDTO, Depends(get_user_from_http_request)]) -> UserId:
    return user.id
