from typing import Annotated

from fastapi import Depends

from sqlalchemy.orm import Session

from eshop import settings

from framework.ddd.dto import DTO
from framework.fastapi.dependencies.get_use_from_request import get_user_from_http_request

from user_identity import hints
from user_identity.api_router import api_router
from user_identity.domain.models.user.user_repository import UserRepository

__all__ = ('profile_view__get', )


class ProfileDTO(DTO):

    id: hints.UserId
    name: hints.UserName


@api_router.get('/profile/')
def profile_view__get(user_id: Annotated[hints.UserId, Depends(get_user_from_http_request)]) -> ProfileDTO:
    with Session(settings.SQLALCHEMY_ENGINE) as session:
        user = UserRepository(session=session).get_by_id(id=user_id)

    return ProfileDTO(id=user.id, name=user.name)
