from fastapi import APIRouter

from basket.app_config import BasketAppConfig

api_router = APIRouter(
    prefix=f'/{BasketAppConfig.name}',
    tags=[
        BasketAppConfig.name,
    ],
)
