from typing import Annotated

from fastapi import Depends, HTTPException, status

from eshop.settings import settings

from framework.cqrs.exceptions import UnexpectedError

from user_identity_cqrs_contract import hints
from user_identity_cqrs_contract.query import UserIdFromJWTTokenQuery
from user_identity_cqrs_contract.query.query import InvalidJwtTokenError


def get_user_from_http_request(jwt_token: Annotated[hints.JWTToken, Depends(settings.OAUTH2_SCHEME)]) -> hints.UserId:
    try:
        return UserIdFromJWTTokenQuery(jwt_token=jwt_token).fetch().id
    except InvalidJwtTokenError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid jwt token')
    except UnexpectedError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
