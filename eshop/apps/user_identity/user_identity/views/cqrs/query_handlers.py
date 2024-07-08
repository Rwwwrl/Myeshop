from eshop import settings

from framework.cqrs.query.handler import IQueryHandler

from user_identity.dependency_container import dependency_container
from user_identity.services.jwt_encoder_decoder import DecodeError

from user_identity_cqrs_contract.hints import UserId
from user_identity_cqrs_contract.query import UserIdFromJWTTokenQuery
from user_identity_cqrs_contract.query.query import InvalidJwtTokenError

__all__ = ('UserFromJWTTokenQueryHandler', )


@UserIdFromJWTTokenQuery.handler
class UserFromJWTTokenQueryHandler(IQueryHandler):
    def handle(self, query: UserIdFromJWTTokenQuery) -> UserId:
        jwt_encoder_decoder = dependency_container.jwt_encoder_decoder_factory()
        try:
            return jwt_encoder_decoder.decode(
                token=query.jwt_token,
                secret=settings.SETTINGS.user_identity_service.secret,
            )
        except DecodeError:
            raise InvalidJwtTokenError
