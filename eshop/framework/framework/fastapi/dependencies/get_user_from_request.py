from typing import Annotated

from fastapi import Depends

from eshop.settings import settings

from framework.cqrs.exceptions import UnexpectedError
from framework.fastapi.http_exceptions import BadRequestException, InternalServerError

from user_identity_cqrs_contract import hints
from user_identity_cqrs_contract.query import UserIdFromJWTTokenQuery
from user_identity_cqrs_contract.query.query import InvalidJwtTokenError


def get_user_from_http_request(jwt_token: Annotated[hints.JWTToken, Depends(settings.OAUTH2_SCHEME)]) -> hints.UserId:
    try:
        return UserIdFromJWTTokenQuery(jwt_token=jwt_token).fetch().id
    except InvalidJwtTokenError:
        raise BadRequestException(detail='invalid jwt token')
    except UnexpectedError:
        raise InternalServerError()
