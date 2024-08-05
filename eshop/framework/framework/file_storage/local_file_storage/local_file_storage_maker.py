import os
from functools import partial

from eshop import settings

from .local_file_storage import LocalFileStorage

MEDIAFILES_DIR = settings.BASE_DIR.parent / 'media'
os.makedirs(MEDIAFILES_DIR, exist_ok=True)

LocalFileStorage = partial(LocalFileStorage, media_root=MEDIAFILES_DIR)
