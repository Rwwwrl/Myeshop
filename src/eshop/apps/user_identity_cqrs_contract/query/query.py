from eshop.framework.cqrs.query import Query

from user_identity_cqrs_contract.types import JWTToken

from .query_response import UserDTO

__all__ = ('UserIdFromJWTTokenQuery', )


class UserIdFromJWTTokenQuery(Query[UserDTO]):

    jwt_token: JWTToken
