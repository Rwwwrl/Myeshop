import abc
from typing import BinaryIO, NewType, Optional

from pydantic import ConfigDict, SkipValidation

from framework.common.dto import DTO

__all__ = (
    'UploadFile',
    'IFileStorageApi',
)

UrlPathToFile = NewType('UrlPathToFile', str)

Filename = NewType('Filename', str)


class UploadFile(DTO):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    file: SkipValidation[BinaryIO]
    filename: str


class IFileStorageApi(abc.ABC):
    @abc.abstractmethod
    def url_path_for_file(self, filename: Filename) -> UrlPathToFile:
        raise NotImplementedError

    @abc.abstractmethod
    def upload(self, upload_file: UploadFile) -> UrlPathToFile:
        raise NotImplementedError

    @abc.abstractmethod
    def update(
        self,
        old_file_filename: str,
        upload_file: UploadFile,
        does_not_exist_ok: Optional[bool] = False,
    ) -> UrlPathToFile:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, url_path_to_file: UrlPathToFile) -> None:
        raise NotImplementedError
