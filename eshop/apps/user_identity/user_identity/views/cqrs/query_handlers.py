from eshop import settings

from framework.cqrs.query.handler import IQueryHandler
from framework.sqlalchemy.session import Session

from user_identity.dependency_container import dependency_container
from user_identity.infrastructure.peristance.user import (
    UserRepository,
    user_repository as user_repository_module,
)
from user_identity.services.jwt_encoder_decoder import DecodeError

from user_identity_cqrs_contract.hints import UserId
from user_identity_cqrs_contract.query import (
    UserIdFromJWTTokenQuery,
    UserQuery,
)
from user_identity_cqrs_contract.query.query import (
    InvalidJwtTokenError,
    UserNotFoundError,
)
from user_identity_cqrs_contract.query.query_response import (
    UserDTO,
)

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
            raise InvalidJwtTokenError(f'jwt_token = {query.jwt_token}')


@UserQuery.handler
class UserQueryHandler(IQueryHandler):
    def handle(self, query: UserQuery) -> UserDTO:
        with Session() as session:
            user_repository = UserRepository(session=session)
            try:
                with session.begin():
                    user = user_repository.get_by_id(id=query.user_id)
            except user_repository_module.NotFoundError:
                raise UserNotFoundError(f'user_id = {query.user_id}')

        return UserDTO(id=user.id, name=user.name)
