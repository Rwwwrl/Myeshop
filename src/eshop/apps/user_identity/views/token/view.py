from datetime import datetime
from enum import Enum
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import jwt

import pytz

from sqlalchemy.orm import Session

from eshop import settings
from eshop.apps.user_identity import hints
from eshop.apps.user_identity.api_router import api_router
from eshop.apps.user_identity.dependency_container import dependency_container
from eshop.apps.user_identity.domain.models.user import User
from eshop.apps.user_identity.domain.models.user.user_repository import NotFoundInDB, UserRepository
from eshop.framework.ddd.dto import DTO

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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


def create_jwt_token(user_id: hints.UserId) -> hints.JWTToken:
    expire_at = datetime.now(tz=pytz.UTC) + settings.SETTINGS.user_identity_service_settings.token_life_time_duration
    payload = {'sub': str(user_id), 'exp': expire_at}
    return jwt.encode(
        claims=payload,
        key=settings.SETTINGS.user_identity_service_settings.secret,
        algorithm='HS256',
    )


def login(username: hints.UserName, password: hints.PlainPassword) -> hints.JWTToken:
    user = authenticate(user_name=username, plain_password=password)
    return create_jwt_token(user_id=user.id)


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

    return AccessTokenDTO(acess_token=jwt_token, token_type=TokenType.bearer)
