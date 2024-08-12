from typing import Annotated

from fastapi import Depends

from framework.common.dto import DTO
from framework.fastapi.dependencies.get_user_id_from_http_request import get_user_id_from_http_request
from framework.sqlalchemy.session import Session

from user_identity import hints
from user_identity.api_router import api_router
from user_identity.domain.models.user import UserRepository

__all__ = ('profile', )


class ProfileDTO(DTO):

    id: hints.UserId
    name: hints.UserName


@api_router.get('/profile/')
def profile(user_id: Annotated[hints.UserId, Depends(get_user_id_from_http_request)]) -> ProfileDTO:
    with Session() as session:
        with session.begin():
            user = UserRepository(session=session).get_by_id(id=user_id)

    return ProfileDTO(id=user.id, name=user.name)
