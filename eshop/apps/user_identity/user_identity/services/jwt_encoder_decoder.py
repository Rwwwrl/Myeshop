import abc
from datetime import datetime
from typing import final

from jose import JWTError, jwt

from user_identity import hints


class DecodeError(Exception):
    pass


class IJWTEncoderDecoder(abc.ABC):
    @abc.abstractmethod
    def encode(self, user_id: hints.UserId, expire_at: datetime, secret: str) -> hints.JWTToken:
        raise NotImplementedError

    @abc.abstractmethod
    def decode(self, token: hints.JWTToken, secret: str) -> hints.UserId:
        raise NotImplementedError


@final
class JoseJWTEncoderDecoder(IJWTEncoderDecoder):
    def __init__(self):
        self._algorithm = 'HS256'

    def encode(self, user_id: hints.UserId, expire_at: datetime, secret: str) -> hints.JWTToken:
        payload = {'sub': str(user_id), 'exp': expire_at}
        return jwt.encode(
            claims=payload,
            key=secret,
            algorithm=self._algorithm,
        )

    def decode(self, token: hints.JWTToken, secret: str) -> hints.UserId:
        try:
            payload = jwt.decode(
                token=token,
                key=secret,
                algorithms=[
                    self._algorithm,
                ],
            )
        except JWTError as e:
            raise DecodeError(e)

        try:
            user_id = int(payload['sub'])
        except (KeyError, ValueError):
            raise DecodeError

        return user_id
