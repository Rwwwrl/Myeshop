from dependency_injector import containers, providers

from framework.file_storage.local_file_storage_api import LocalFileStorageApi


class DependencyContainer(containers.DeclarativeContainer):
    file_storage_api_factory = providers.Singleton(LocalFileStorageApi)


dependency_container = DependencyContainer()
