from typing import Final, final

from attrs import define

from framework.cqrs.exceptions import PossibleExpectedError
from framework.cqrs.query.query import Query

from user_identity_cqrs_contract.hints import JWTToken, UserId

from .query_response import UserDTO, UserIdWithRoleDTO

__all__ = (
    'UserFromJWTTokenQuery',
    'UserQuery',
)


@final
class InvalidJwtTokenError(PossibleExpectedError):
    pass


@final
@define
class UserFromJWTTokenQuery(Query[UserIdWithRoleDTO]):

    jwt_token: JWTToken

    __possible_exceptions__: Final = (InvalidJwtTokenError, )


@final
class UserNotFoundError(PossibleExpectedError):
    pass


@final
@define
class UserQuery(Query[UserDTO]):

    user_id: UserId

    __possible_exceptions__: Final = (UserNotFoundError, )
