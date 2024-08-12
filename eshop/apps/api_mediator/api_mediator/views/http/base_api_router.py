from fastapi import APIRouter

from api_mediator.app_config import ApiMediatorAppConfig

base_api_router = APIRouter(
    prefix=f'/{ApiMediatorAppConfig.name}',
    tags=[
        ApiMediatorAppConfig.name,
    ],
)
