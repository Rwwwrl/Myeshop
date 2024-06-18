from typing import Final

from attrs import define

from framework.cqrs.exceptions import PossibleExpectedError
from framework.cqrs.query.query import Query

from user_identity_cqrs_contract.hints import JWTToken

from .query_response import UserDTO

__all__ = ('UserIdFromJWTTokenQuery', )


class InvalidJwtTokenError(PossibleExpectedError):
    pass


@define
class UserIdFromJWTTokenQuery(Query[UserDTO]):

    jwt_token: JWTToken

    __possible_exceptions__: Final = (InvalidJwtTokenError, )
