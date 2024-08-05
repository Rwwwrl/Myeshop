import os
from pathlib import Path

from ..ifile_storage import IFileStorage, UploadFile


class LocalFileStorage(IFileStorage):
    def __init__(self, media_root: Path):
        self._media_root = media_root

    def upload(self, upload_file: UploadFile, space: str) -> None:
        os.makedirs(self._media_root / space, exist_ok=True)
        with open(self._media_root / space / upload_file.filename, 'wb') as file:
            file.write(upload_file.file.read())
