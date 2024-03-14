from framework.cqrs.query import Query

from user_identity_cqrs_contract.hints import JWTToken

from .query_response import UserDTO

__all__ = ('UserIdFromJWTTokenQuery', )


class UserIdFromJWTTokenQuery(Query[UserDTO]):

    jwt_token: JWTToken
