import abc

from passlib.context import CryptContext

from eshop.apps.user_identity import hints


class IPasswordHasher(abc.ABC):
    @abc.abstractmethod
    def hash(self, plain_password: hints.PlainPassword) -> hints.HashedPassword:
        raise NotImplementedError

    @abc.abstractmethod
    def verify(self, plain_password: hints.PlainPassword, hashed_password: hints.HashedPassword) -> bool:
        raise NotImplementedError


class PasslibPasswordHasher(IPasswordHasher):
    def __init__(self):
        self._context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, plain_password: hints.PlainPassword) -> hints.HashedPassword:
        return self._context.hash(plain_password)

    def verify(self, plain_password: hints.PlainPassword, hashed_password: hints.HashedPassword) -> bool:
        return self._context.verify(plain_password, hashed_password)
