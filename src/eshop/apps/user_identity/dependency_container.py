from dependency_injector import containers, providers

from user_identity.services.jwt_encoder_decoder import JoseJWTEncoderDecoder
from user_identity.services.password_hasher import PasslibPasswordHasher


class DependencyContainer(containers.DeclarativeContainer):
    password_hasher_factory = providers.Singleton(PasslibPasswordHasher)
    jwt_encoder_decoder_factory = providers.Singleton(JoseJWTEncoderDecoder)


dependency_container = DependencyContainer()
