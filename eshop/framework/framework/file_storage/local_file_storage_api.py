import os
from pathlib import Path

from eshop import settings

from .ifile_storage_api import (
    Filename,
    IFileStorageApi,
    UploadFile,
    UrlPathToFile,
)

__all__ = ('LocalFileStorageApi')


class LocalFileStorage:
    def __init__(self, media_root: Path):
        self._media_root = media_root
        os.makedirs(self._media_root, exist_ok=True)

    def save(self, upload_file: UploadFile) -> None:
        with open(self._media_root / upload_file.filename, 'wb') as file:
            file.write(upload_file.file.read())

    def remove(self, filename: Filename) -> None:
        os.remove(self._media_root / filename)


class LocalFileStorageApi(IFileStorageApi):
    def __init__(self):
        self._file_storage = LocalFileStorage(media_root=settings.BASE_DIR.parent / settings.MEDIA_ROOT_URL)

    def url_path_for_file(self, filename: Filename) -> UrlPathToFile:
        return f'{settings.MEDIA_ROOT_URL}/{filename}'

    def upload(self, upload_file: UploadFile) -> UrlPathToFile:
        self._file_storage.save(upload_file=upload_file)
        return self.url_path_for_file(filename=upload_file.filename)

    def delete(self, url_path_to_file: UrlPathToFile) -> None:
        filename = url_path_to_file.split('/')[-1]
        self._file_storage.remove(filename=filename)
