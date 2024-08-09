from typing import final

from eshop import settings

from framework.cqrs.query.handler import IQueryHandler
from framework.sqlalchemy.session import Session

from user_identity.dependency_container import dependency_container
from user_identity.domain.models.user.user_repository import NotFoundError, UserRepository
from user_identity.services.jwt_encoder_decoder import DecodeError

from user_identity_cqrs_contract.hints import UserId
from user_identity_cqrs_contract.query import (
    UserByIdQuery,
    UserFromJWTTokenQuery,
)
from user_identity_cqrs_contract.query.query import (
    InvalidJwtTokenError,
    UserNotFoundError,
)
from user_identity_cqrs_contract.query.query_response import (
    UserDTO,
    UserIdWithRoleDTO,
    UserRoleEnum,
)

__all__ = ('UserFromJWTTokenQueryHandler', )


@final
@UserFromJWTTokenQuery.handler
class UserFromJWTTokenQueryHandler(IQueryHandler):
    def handle(self, query: UserFromJWTTokenQuery) -> UserId:
        jwt_encoder_decoder = dependency_container.jwt_encoder_decoder_factory()
        try:
            user_id = jwt_encoder_decoder.decode(
                token=query.jwt_token,
                secret=settings.SETTINGS.user_identity_service.secret,
            )
        except DecodeError:
            raise InvalidJwtTokenError(f'jwt_token = {query.jwt_token}')

        with Session() as session:
            user_repository = UserRepository(session=session)
            with session.begin():
                user = user_repository.get_by_id(id=user_id)
                return UserIdWithRoleDTO(id=user.id, role=UserRoleEnum[user.role.value])


@final
@UserByIdQuery.handler
class UserByIdQueryHandler(IQueryHandler):
    def handle(self, query: UserByIdQuery) -> UserDTO:
        with Session() as session:
            user_repository = UserRepository(session=session)
            try:
                with session.begin():
                    user = user_repository.get_by_id(id=query.id)
            except NotFoundError:
                raise UserNotFoundError(f'user_id = {query.id}')

        return UserDTO(id=user.id, name=user.name)
