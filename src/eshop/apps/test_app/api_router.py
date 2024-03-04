from fastapi import APIRouter

from .app_config import TestAppConfig

api_router = APIRouter(
    prefix=f'/{TestAppConfig.name}',
    tags=[
        TestAppConfig.name,
    ],
)
