from datetime import datetime
from enum import Enum
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

import pytz

from sqlalchemy.orm import Session

from eshop import settings

from framework.common.dto import DTO

from user_identity import hints
from user_identity.api_router import api_router
from user_identity.dependency_container import dependency_container
from user_identity.domain.models.user import User
from user_identity.domain.models.user.user_repository import NotFoundInDB, UserRepository

__all__ = ('token_view', )


class TokenType(Enum):

    bearer = 'bearer'


class AccessTokenDTO(DTO):
    access_token: hints.JWTToken
    token_type: TokenType


class AuthenticateException(Exception):
    pass


def authenticate(user_name: hints.UserName, plain_password: hints.PlainPassword) -> User:
    with Session(settings.SQLALCHEMY_ENGINE) as session:
        try:
            user = UserRepository(session=session).get_by_name(name=user_name)
        except NotFoundInDB:
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
def token_view(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> AccessTokenDTO:
    try:
        jwt_token = login(username=form_data.username, password=form_data.password)
    except AuthenticateException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return AccessTokenDTO(access_token=jwt_token, token_type=TokenType.bearer)
