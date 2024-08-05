import abc
from typing import BinaryIO

from pydantic import ConfigDict, SkipValidation

from framework.common.dto import DTO

__all__ = (
    'UploadFile',
    'IFileStorage',
)


class UploadFile(DTO):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    file: SkipValidation[BinaryIO]
    filename: str


class IFileStorage(abc.ABC):
    @abc.abstractmethod
    def upload(self, upload_file: UploadFile, space: str) -> None:
        raise NotImplementedError
