from dependency_injector import containers, providers

from eshop.apps.user_identity.services.password_hasher import PasslibPasswordHasher


class DependencyContainer(containers.DeclarativeContainer):
    password_hasher_factory = providers.Singleton(PasslibPasswordHasher)


dependency_container = DependencyContainer()
