from typing import Annotated

from fastapi import Depends

from eshop.settings import settings

from framework.cqrs.exceptions import UnexpectedError
from framework.fastapi.http_exceptions import BadRequestException, InternalServerError

from user_identity_cqrs_contract import hints
from user_identity_cqrs_contract.query import UserFromJWTTokenQuery
from user_identity_cqrs_contract.query.query import InvalidJwtTokenError
from user_identity_cqrs_contract.query.query_response import UserIdWithRoleDTO


def get_user_from_http_request(
    jwt_token: Annotated[hints.JWTToken, Depends(settings.OAUTH2_SCHEME)],
) -> UserIdWithRoleDTO:
    try:
        return UserFromJWTTokenQuery(jwt_token=jwt_token).fetch()
    except InvalidJwtTokenError:
        raise BadRequestException(detail='invalid jwt token')
    except UnexpectedError:
        raise InternalServerError()
