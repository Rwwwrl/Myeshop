from fastapi import APIRouter

from .app_config import ApiGatewayAppConfig

api_router = APIRouter(
    prefix=f'/{ApiGatewayAppConfig.name}',
    tags=[
        ApiGatewayAppConfig.name,
    ],
)
