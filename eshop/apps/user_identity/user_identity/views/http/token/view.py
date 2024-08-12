from datetime import datetime
from enum import Enum
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

import pytz

from eshop import settings

from framework.common.dto import DTO
from framework.sqlalchemy.session import Session

from user_identity import hints
from user_identity.dependency_container import dependency_container
from user_identity.domain.models.user import User, UserRepository
from user_identity.domain.models.user.user_repository import NotFoundError
from user_identity.views.http.api_router import api_router

__all__ = ('token', )


class TokenType(Enum):

    bearer = 'bearer'


class AccessTokenDTO(DTO):
    access_token: hints.JWTToken
    token_type: TokenType


class AuthenticateException(Exception):
    pass


def authenticate(user_name: hints.UserName, plain_password: hints.PlainPassword) -> User:
    with Session() as session:
        try:
            with session.begin():
                user = UserRepository(session=session).get_by_name(name=user_name)
        except NotFoundError:
            raise AuthenticateException(f'reason: there is not user with name = {user_name}')

    password_hasher = dependency_container.password_hasher_factory()
    if not password_hasher.verify(plain_password=plain_password, hashed_password=user.hashed_password):
        raise AuthenticateException('reason: wrong password')

    return user


def login(username: hints.UserName, password: hints.PlainPassword) -> hints.JWTToken:
    user = authenticate(user_name=username, plain_password=password)
    jwt_encoder_decoder = dependency_container.jwt_encoder_decoder_factory()
    expire_at = datetime.now(tz=pytz.UTC) + settings.SETTINGS.user_identity_service.token_life_time_duration
    return jwt_encoder_decoder.encode(
        user_id=user.id,
        expire_at=expire_at,
        secret=settings.SETTINGS.user_identity_service.secret,
    )


@api_router.post("/token/")
def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> AccessTokenDTO:
    try:
        jwt_token = login(username=form_data.username, password=form_data.password)
    except AuthenticateException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return AccessTokenDTO(access_token=jwt_token, token_type=TokenType.bearer)
