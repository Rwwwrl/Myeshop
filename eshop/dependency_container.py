from dependency_injector import containers, providers

from framework.cqrs.cqrs_bus import CQRSBus
from framework.file_storage.local_file_storage_api import LocalFileStorageApi


class DependencyContainer(containers.DeclarativeContainer):
    file_storage_api_factory = providers.Singleton(LocalFileStorageApi)
    cqrs_bus_factory = providers.Singleton(CQRSBus)


dependency_container = DependencyContainer()
