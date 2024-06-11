from attrs import define

from framework.cqrs.query.query import Query

from user_identity_cqrs_contract.hints import JWTToken

from .query_response import UserDTO

__all__ = ('UserIdFromJWTTokenQuery', )


@define
class UserIdFromJWTTokenQuery(Query[UserDTO]):

    jwt_token: JWTToken
