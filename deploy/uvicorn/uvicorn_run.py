import multiprocessing

import uvicorn

workers = multiprocessing.cpu_count() * 2 + 1

if __name__ == '__main__':
    uvicorn.run(
        app='eshop.settings:MAIN_APP',
        reload=False,
        uds='/usr/uvicorn_socket_folder/uvicorn.sock',
        workers=workers,
    )
