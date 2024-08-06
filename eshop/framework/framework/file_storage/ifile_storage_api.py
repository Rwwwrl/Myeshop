import abc
from typing import BinaryIO, NewType

from pydantic import ConfigDict, SkipValidation

from framework.common.dto import DTO

__all__ = (
    'UploadFile',
    'IFileStorageApi',
)

UrlPathToFile = NewType('UrlPathToFile', str)


class UploadFile(DTO):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    file: SkipValidation[BinaryIO]
    filename: str


class IFileStorageApi(abc.ABC):
    @abc.abstractmethod
    def upload(self, upload_file: UploadFile) -> UrlPathToFile:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, url_path_to_file: UrlPathToFile) -> None:
        raise NotImplementedError
