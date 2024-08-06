import os
from pathlib import Path
from typing import NewType

from eshop import settings

from .ifile_storage_api import IFileStorageApi, UploadFile, UrlPathToFile

__all__ = ('LocalFileStorageApi')

Filename = NewType('Filename', str)


class LocalFileStorage:
    def __init__(self, media_root: Path):
        self._media_root = media_root
        os.makedirs(self._media_root, exist_ok=True)

    def save(self, upload_file: UploadFile) -> Filename:
        with open(self._media_root / upload_file.filename, 'wb') as file:
            file.write(upload_file.file.read())

        return upload_file.filename


class LocalFileStorageApi(IFileStorageApi):
    def __init__(self):
        self._file_storage = LocalFileStorage(media_root=settings.BASE_DIR.parent / settings.MEDIA_ROOT_URL)

    def upload(self, upload_file: UploadFile) -> UrlPathToFile:
        filename = self._file_storage.save(upload_file=upload_file)
        return f'{settings.MEDIA_ROOT_URL}/{filename}'
