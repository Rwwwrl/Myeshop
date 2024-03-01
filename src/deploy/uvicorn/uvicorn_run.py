import multiprocessing

import uvicorn

workers = multiprocessing.cpu_count() * 2 + 1

if __name__ == '__main__':
    uvicorn.run(
        app='eshop.settings:MAIN_APP',
        reload=False,
        host='0.0.0.0',
        port=80,
        workers=workers,
        access_log='-',
    )
