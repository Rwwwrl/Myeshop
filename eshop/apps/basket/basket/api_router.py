from fastapi import APIRouter

from .app_config import BasketAppConfig

api_router = APIRouter(
    prefix=f'/{BasketAppConfig.name}',
    tags=[
        BasketAppConfig.name,
    ],
)
