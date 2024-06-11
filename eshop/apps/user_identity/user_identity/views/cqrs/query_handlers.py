from eshop import settings

from framework.cqrs.query.handler import IQueryHandler

from user_identity.dependency_container import dependency_container

from user_identity_cqrs_contract.query.query import UserIdFromJWTTokenQuery
from user_identity_cqrs_contract.query.query_response import UserDTO

__all__ = ('UserFromJWTTokenQueryHandler', )


@UserIdFromJWTTokenQuery.handler
class UserFromJWTTokenQueryHandler(IQueryHandler):
    def handle(self, query: UserIdFromJWTTokenQuery) -> UserDTO:
        jwt_encoder_decoder = dependency_container.jwt_encoder_decoder_factory()
        user_id = jwt_encoder_decoder.decode(
            token=query.jwt_token,
            secret=settings.SETTINGS.user_identity_service.secret,
        )
        return UserDTO(id=user_id)
