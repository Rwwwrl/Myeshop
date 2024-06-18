from fastapi import APIRouter

from .app_config import ApiGatewayAppConfig

base_api_router = APIRouter(
    prefix=f'/{ApiGatewayAppConfig.name}',
    tags=[
        ApiGatewayAppConfig.name,
    ],
)
