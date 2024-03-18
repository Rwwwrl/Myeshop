from framework.cqrs.query.query import Query, query

from user_identity_cqrs_contract.hints import JWTToken

from .query_response import UserDTO

__all__ = ('UserIdFromJWTTokenQuery', )


@query(UserDTO)
class UserIdFromJWTTokenQuery(Query):

    jwt_token: JWTToken
