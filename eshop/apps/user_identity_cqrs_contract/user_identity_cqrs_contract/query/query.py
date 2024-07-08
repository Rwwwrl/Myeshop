from typing import Final, final

from attrs import define

from framework.cqrs.exceptions import PossibleExpectedError
from framework.cqrs.query.query import Query

from user_identity_cqrs_contract.hints import JWTToken, UserId

__all__ = ('UserIdFromJWTTokenQuery', )


@final
class InvalidJwtTokenError(PossibleExpectedError):
    pass


@final
@define
class UserIdFromJWTTokenQuery(Query[UserId]):

    jwt_token: JWTToken

    __possible_exceptions__: Final = (InvalidJwtTokenError, )
