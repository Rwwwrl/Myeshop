import multiprocessing
from pathlib import Path
from typing import NoReturn

import uvicorn

workers = multiprocessing.cpu_count() * 2 + 1

UVICORN_SOCKET_PATH = Path('/usr/uvicorn_socket_folder/uvicorn.sock')


def main() -> NoReturn:
    UVICORN_SOCKET_PATH.unlink(missing_ok=True)
    uvicorn.run(
        app='eshop.settings:MAIN_APP',
        reload=False,
        uds=UVICORN_SOCKET_PATH.as_posix(),
        workers=workers,
    )


if __name__ == '__main__':
    main()
