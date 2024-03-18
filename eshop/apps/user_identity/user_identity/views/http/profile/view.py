from typing import Annotated

from fastapi import Depends

from sqlalchemy.orm import Session

from eshop import settings

from framework.ddd.dto import DTO

from user_identity import hints
from user_identity.api_router import api_router
from user_identity.domain.models.user.user_repository import UserRepository

from user_identity_cqrs_contract.query import UserIdFromJWTTokenQuery

__all__ = ('profile_view__get', )


class ProfileDTO(DTO):

    id: hints.UserId
    name: hints.UserName


@api_router.get('/profile/')
def profile_view__get(jwt_token: Annotated[hints.JWTToken, Depends(settings.OAUTH2_SCHEME)]) -> ProfileDTO:
    user_id = UserIdFromJWTTokenQuery(jwt_token=jwt_token).fetch().id

    with Session(settings.SQLALCHEMY_ENGINE) as session:
        user = UserRepository(session=session).get_by_id(id=user_id)

    return ProfileDTO(id=user.id, name=user.name)
