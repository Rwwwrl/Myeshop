from fastapi import APIRouter

from .app_config import UserIdentityAppConfig

api_router = APIRouter(
    prefix=f'/{UserIdentityAppConfig.name}',
    tags=[
        UserIdentityAppConfig.name,
    ],
)
