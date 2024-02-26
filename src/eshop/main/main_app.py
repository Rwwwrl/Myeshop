from eshop.test_app.views import router as test_app_router

from fastapi import FastAPI

MAIN_APP = FastAPI()

MAIN_APP.include_router(test_app_router, prefix='', tags=['test_app'])
